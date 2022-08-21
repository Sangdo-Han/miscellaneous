# reuse almost every functions in utils.traine
if __name__ == "sanhan_addons.trainer":
    from utils.trainer import *
else:
    from ..utils.trainer import *

import numpy as np
# override function

def mixup_train_single_batch(net: nn.Module, 
                            data: torch.Tensor, 
                            targets: torch.Tensor, 
                            optimizer: optim.Optimizer, 
                            criterion: Callable, 
                            device: torch.device) -> Tuple[float, int]:

    data, targets = data.to(device), targets.to(device)

    # apply mixup
    if np.random.random() > 0.5:
        lmbd= np.random.beta(a=0.5, b=0.5)
    else: 
        lmbd = 0
    mini_batch_indices = list(range(len(data)))
    mix_batch_indices = list(range(len(data)))
    np.random.shuffle(mix_batch_indices)

    # mixup on data
    data = (1-lmbd) * data[mini_batch_indices] + lmbd * data[mix_batch_indices]
    optimizer.zero_grad()
    outputs = net(data)
    softmax_outputs = outputs.log_softmax(dim=criterion.dim)
    with torch.no_grad():
        onehot_targets = torch.zeros_like(softmax_outputs)
        onehot_targets.fill_(criterion.smoothing / (criterion.cls -1 ))
        onehot_targets.scatter_(1, targets.data.unsqueeze(1), criterion.confidence)
        # mixup on targets
        onehot_targets = (1-lmbd) * onehot_targets[mini_batch_indices] + \
            lmbd * onehot_targets[mix_batch_indices]

    loss = torch.mean(torch.sum(-onehot_targets * softmax_outputs, dim=criterion.dim))
    loss.backward()
    optimizer.step()

    correct = outputs.argmax(1).eq(targets).sum()
    return loss.item(), correct.item()

def train(net: nn.Module, optimizer: optim.Optimizer, criterion: Callable, trainloader: DataLoader, valloader: DataLoader, schedulers: dict, config: dict) -> None:
    """Trains model.

    Args:
        net (nn.Module): Model instance.
        optimizer (optim.Optimizer): Optimizer instance.
        criterion (Callable): Loss function.
        trainloader (DataLoader): Training data loader.
        valloader (DataLoader): Validation data loader.
        schedulers (dict): Dict containing schedulers.
        config (dict): Config dict.
    """
    
    step = 0
    best_acc = 0.0
    n_batches = len(trainloader)
    device = config["hparams"]["device"]
    log_file = os.path.join(config["exp"]["save_dir"], "training_log.txt")
    
    ############################
    # start training
    ############################
    net.train()
    
    for epoch in range(config["hparams"]["n_epochs"]):
        t0 = time.time()
        running_loss = 0.0
        correct = 0

        for batch_index, (data, targets) in enumerate(trainloader):

            if schedulers["warmup"] is not None and epoch < config["hparams"]["scheduler"]["n_warmup"]:
                schedulers["warmup"].step()

            elif schedulers["scheduler"] is not None:
                schedulers["scheduler"].step()

            ####################
            # optimization step
            ####################

            loss, corr = mixup_train_single_batch(net, data, targets, optimizer, criterion, device)
            running_loss += loss
            correct += corr

            if not step % config["exp"]["log_freq"]:       
                log_dict = {"epoch": epoch, "loss": loss, "lr": optimizer.param_groups[0]["lr"]}
                log(log_dict, step, config)

            step += 1
            
        #######################
        # epoch complete
        #######################

        log_dict = {"epoch": epoch, "time_per_epoch": time.time() - t0, "train_acc": correct/(len(trainloader.dataset)), "avg_loss_per_ep": running_loss/len(trainloader)}
        log(log_dict, step, config)

        if not epoch % config["exp"]["val_freq"]:
            val_acc, avg_val_loss = evaluate(net, criterion, valloader, device)
            log_dict = {"epoch": epoch, "val_loss": avg_val_loss, "val_acc": val_acc}
            log(log_dict, step, config)

            # save best val ckpt
            if val_acc > best_acc:
                best_acc = val_acc
                save_path = os.path.join(config["exp"]["save_dir"], "best.pth")
                save_model(epoch, val_acc, save_path, net, optimizer, log_file) 

    ###########################
    # training complete
    ###########################

    val_acc, avg_val_loss = evaluate(net, criterion, valloader, device)
    log_dict = {"epoch": epoch, "val_loss": avg_val_loss, "val_acc": val_acc}
    log(log_dict, step, config)

    # save final ckpt
    save_path = os.path.join(config["exp"]["save_dir"], "last.pth")
    save_model(epoch, val_acc, save_path, net, optimizer, log_file)