import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import time
import random
import multiprocessing
import os
import concurrent.futures # Multiprocessing 아니어도 ProcessPool 사용 가능

import numpy as np

class Ball:
    def __init__(self, id, pos, vel, radius=0.1, color=(1.0, 1.0, 1.0)):
        self.id = id
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(vel, dtype=float)
        self.radius = radius
        self.color = np.array(color, dtype=float)
        self.mass = radius**3 * np.pi * (4/3) # 질량은 반지름의 세제곱에 비례한다고 가정

    def update_position(self, dt):
        self.pos += self.vel * dt

    def check_wall_collision(self, bounds):
        """벽과의 충돌 감지 및 처리"""
        for i in range(3): # x, y, z
            if self.pos[i] - self.radius < bounds[0][i]:
                self.pos[i] = bounds[0][i] + self.radius
                self.vel[i] *= -1.0 # 반사
            elif self.pos[i] + self.radius > bounds[1][i]:
                self.pos[i] = bounds[1][i] - self.radius
                self.vel[i] *= -1.0 # 반사

    def check_ball_collision(self, other_ball):
        """다른 공과의 충돌 감지 및 처리 (탄성 충돌)"""
        dist_vec = other_ball.pos - self.pos
        distance = np.linalg.norm(dist_vec)

        if distance <= self.radius + other_ball.radius and distance > 0:
            # 충돌 발생
            normal_vec = dist_vec / distance
            
            # 상대 속도
            relative_vel = other_ball.vel - self.vel
            
            # 충돌 방향에 대한 상대 속도 성분
            vel_along_normal = np.dot(relative_vel, normal_vec)
            
            # 이미 멀어지고 있다면 충돌 처리 안 함 (부동 소수점 오류 방지)
            if vel_along_normal > 0:
                return

            # 충격량 계산 (탄성 충돌 공식)
            e = 1.0 # 반발 계수 (완전 탄성 충돌)
            impulse = (-(1 + e) * vel_along_normal) / ((1 / self.mass) + (1 / other_ball.mass))
            
            impulse_vec = impulse * normal_vec

            # 속도 업데이트
            self.vel -= impulse_vec / self.mass
            other_ball.vel += impulse_vec / other_ball.mass

            # 겹침 방지 (약간 밀어냄)
            overlap = (self.radius + other_ball.radius) - distance
            if overlap > 0:
                correction = overlap / 2.0 * normal_vec
                self.pos -= correction
                other_ball.pos += correction

# 시뮬레이션 경계 (육면체)
BOUNDS_MIN = np.array([-1.0, -1.0, -1.0])
BOUNDS_MAX = np.array([1.0, 1.0, 1.0])
SIMULATION_BOUNDS = (BOUNDS_MIN, BOUNDS_MAX)

# 공 상태를 딕셔너리로 직렬화 (프로세스 간 통신용)
def ball_to_dict(ball):
    return {
        'id': ball.id,
        'pos': ball.pos.tolist(),
        'vel': ball.vel.tolist(),
        'radius': ball.radius,
        'color': ball.color.tolist(),
        'mass': ball.mass
    }

# 딕셔너리로부터 Ball 객체 생성
def dict_to_ball(d):
    return Ball(d['id'], d['pos'], d['vel'], d['radius'], d['color'])

# --- OpenGL Drawing Functions (렌더링 프로세스에서 사용) ---
def draw_ball(ball):
    glColor3fv(ball.color)
    glPushMatrix()
    glTranslatef(ball.pos[0], ball.pos[1], ball.pos[2])
    
    sphere = gluNewQuadric()
    gluQuadricDrawStyle(sphere, GLU_FILL)
    gluSphere(sphere, ball.radius, 32, 32)
    gluDeleteQuadric(sphere)
    
    glPopMatrix()

def draw_bounds(bounds_min, bounds_max):
    glColor3f(0.5, 0.5, 0.5) # 회색
    glBegin(GL_LINES)
    # 큐브의 12개 엣지 그리기
    
    # Bottom Face
    glVertex3f(bounds_min[0], bounds_min[1], bounds_min[2])
    glVertex3f(bounds_max[0], bounds_min[1], bounds_min[2])

    glVertex3f(bounds_max[0], bounds_min[1], bounds_min[2])
    glVertex3f(bounds_max[0], bounds_max[1], bounds_min[2])

    glVertex3f(bounds_max[0], bounds_max[1], bounds_min[2])
    glVertex3f(bounds_min[0], bounds_max[1], bounds_min[2])

    glVertex3f(bounds_min[0], bounds_max[1], bounds_min[2])
    glVertex3f(bounds_min[0], bounds_min[1], bounds_min[2])

    # Top Face
    glVertex3f(bounds_min[0], bounds_min[1], bounds_max[2])
    glVertex3f(bounds_max[0], bounds_min[1], bounds_max[2])

    glVertex3f(bounds_max[0], bounds_min[1], bounds_max[2])
    glVertex3f(bounds_max[0], bounds_max[1], bounds_max[2])

    glVertex3f(bounds_max[0], bounds_max[1], bounds_max[2])
    glVertex3f(bounds_min[0], bounds_max[1], bounds_max[2])

    glVertex3f(bounds_min[0], bounds_max[1], bounds_max[2])
    glVertex3f(bounds_min[0], bounds_min[1], bounds_max[2])

    # Connecting Edges
    glVertex3f(bounds_min[0], bounds_min[1], bounds_min[2])
    glVertex3f(bounds_min[0], bounds_min[1], bounds_max[2])

    glVertex3f(bounds_max[0], bounds_min[1], bounds_min[2])
    glVertex3f(bounds_max[0], bounds_min[1], bounds_max[2])

    glVertex3f(bounds_max[0], bounds_max[1], bounds_min[2])
    glVertex3f(bounds_max[0], bounds_max[1], bounds_max[2])

    glVertex3f(bounds_min[0], bounds_max[1], bounds_min[2])
    glVertex3f(bounds_min[0], bounds_max[1], bounds_max[2])
    
    glEnd()

def init_opengl(width, height):
    glClearColor(0.0, 0.0, 0.0, 1.0) # 배경색 검정
    glEnable(GL_DEPTH_TEST) # 깊이 테스트 활성화
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (width / height), 0.1, 50.0) # 원근 투영
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5.0) # 카메라 위치 조정 (뒤로 당기기)

# --- Physics Helper Functions (TOP-LEVEL for pickling) ---

# 공 하나의 위치 업데이트와 벽 충돌 처리 (데이터 분해의 단위)
# dt를 인자로 직접 받도록 수정
def update_ball_state_and_check_wall_collision(ball_dict, dt_val):
    ball = dict_to_ball(ball_dict)
    ball.update_position(dt_val)
    ball.check_wall_collision(SIMULATION_BOUNDS)
    return ball_to_dict(ball)

# --- Physics Process Logic ---
def physics_worker_process(initial_ball_states, dt, shared_data_queue, stop_event):
    """
    물리 계산을 수행하는 별도의 프로세스.
    - 태스크 분해: 메인(렌더링) 프로세스와 분리.
    - 데이터 분해: ProcessPoolExecutor를 사용하여 공들을 병렬 처리.
    """
    balls = [dict_to_ball(s) for s in initial_ball_states]
    print(f"Physics process (PID: {os.getpid()}) started with {len(balls)} balls.")

    # 물리 계산을 위한 ProcessPoolExecutor (데이터 분해 컨셉)
    num_physics_workers = multiprocessing.cpu_count() -1 # 렌더링 프로세스 제외
    if num_physics_workers < 1: num_physics_workers = 1

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_physics_workers) as executor:
        while not stop_event.is_set():
            frame_start_time = time.time()

            # 1. 위치 업데이트 및 벽 충돌 처리 (데이터 병렬)
            # lambda 대신 top-level 함수와 functools.partial을 사용하거나,
            # 아니면 map의 두 번째 인자가 이터러블이므로 튜플로 (ball_dict, dt)를 전달하면 됨.
            # 여기서는 dt_val을 인자로 받는 update_ball_state_and_check_wall_collision 함수를 직접 map에 전달
            
            # map 함수는 하나의 iterable만 받으므로, dt를 각 호출에 전달하기 위해 리스트를 반복하는 방식으로 변환
            # (ball_dict, dt) 튜플 리스트를 생성
            ball_data_for_map = [(ball_to_dict(b), dt) for b in balls]
            
            # executor.map은 각 아이템에 함수를 적용. 이때 함수는 하나의 인자만 받도록 설계되거나,
            # map의 두 번째 인자는 (arg1, arg2, ...) 형태의 튜플이어야 함.
            # update_ball_state_and_check_wall_collision(ball_dict, dt_val)는 두 개의 인자를 받으므로,
            # map에 전달할 때 functools.partial을 사용하거나,
            # 아니면 lambda를 사용하는 대신 helper 함수를 더 명시적으로 정의해야 함.

            # 가장 간단한 해결책: dt를 각 ball_dict에 포함시키거나, map의 두 번째 인자를 활용
            # ProcessPoolExecutor의 map은 여러 이터러블을 인자로 받을 수 있음.
            # executor.map(function, *iterables)
            updated_balls_dicts = list(executor.map(update_ball_state_and_check_wall_collision, 
                                                    [ball_to_dict(b) for b in balls], 
                                                    [dt] * len(balls))) # dt를 각 공에 맞게 반복하여 전달

            balls = [dict_to_ball(d) for d in updated_balls_dicts]

            # 2. 공-공 충돌 처리 (모든 공의 상호작용이 필요하므로 병렬화가 어려움, 순차 처리)
            for i in range(len(balls)):
                for j in range(i + 1, len(balls)):
                    balls[i].check_ball_collision(balls[j])


            # 최신 상태를 메인 프로세스(렌더링)에 전달
            current_states_for_rendering = [ball_to_dict(b) for b in balls]
            
            # 큐가 너무 많이 차는 것을 방지하기 위해 put_nowait 사용 (가장 최신 데이터만 유지)
            try:
                # 큐가 가득 찼다면 이전 데이터는 버리고 최신 데이터로 대체
                while not shared_data_queue.empty():
                    shared_data_queue.get_nowait()
                shared_data_queue.put_nowait(current_states_for_rendering)
            except multiprocessing.queues.Full:
                pass # 큐가 Full이면 그냥 넘어감 (렌더링이 더 느림)
            
            frame_end_time = time.time()
            frame_duration = frame_end_time - frame_start_time
            # 목표 dt를 지키도록 대기 (물리 계산이 너무 빠르면)
            if frame_duration < dt:
                time.sleep(dt - frame_duration)
            
    print("Physics process stopped.")


# --- Main Process (Rendering) ---
def run_multiprocessing_simulation():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Multiprocessing Ball Simulation (Task + Data Decomposition)")

    init_opengl(*display)

    # 공 초기 상태를 직렬화 가능한 형태로 준비 (물리 프로세스로 전달용)
    initial_ball_states = []
    for i in range(150):
        pos = [random.uniform(BOUNDS_MIN[j] + 0.2, BOUNDS_MAX[j] - 0.2) for j in range(3)]
        vel = [random.uniform(-0.5, 0.5) for _ in range(3)]
        color = [random.random() for _ in range(3)]
        initial_ball_states.append(ball_to_dict(Ball(i, pos, vel, radius=0.1, color=color)))
    
    # 프로세스 간 통신을 위한 큐
    ball_data_queue = multiprocessing.Queue(maxsize=10) 

    # 프로세스 종료 시그널
    stop_event = multiprocessing.Event()

    dt = 0.01 # 물리 시뮬레이션의 시간 간격

    # 물리 프로세스 시작 (태스크 분해)
    physics_process = multiprocessing.Process(target=physics_worker_process, 
                                              args=(initial_ball_states, dt, ball_data_queue, stop_event))
    physics_process.start()

    clock = pygame.time.Clock()
    
    render_balls = [] # 렌더링용 공 리스트 (물리 프로세스로부터 데이터를 받아 업데이트)

    main_loop_running = True
    while main_loop_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_loop_running = False

        # --- Rendering (Main Process) ---
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 0, 3,  # 카메라 위치
                  0, 0, 0,  # 바라보는 지점
                  0, 1, 0)  # 업 벡터

        draw_bounds(BOUNDS_MIN, BOUNDS_MAX)
        
        # 물리 프로세스로부터 최신 공 데이터 가져오기
        latest_data_for_rendering = None
        while not ball_data_queue.empty():
            try:
                latest_data_for_rendering = ball_data_queue.get_nowait()
            except multiprocessing.queues.Empty:
                break 

        if latest_data_for_rendering:
            render_balls = [dict_to_ball(state) for state in latest_data_for_rendering]

        for ball in render_balls: 
            draw_ball(ball)
        
        pygame.display.flip()
        # --- End Rendering ---

        clock.tick(144) # 렌더링 프레임 레이트 제한

    # 종료 시그널 보내기
    stop_event.set()
    physics_process.join() # 물리 프로세스가 종료될 때까지 기다림

    pygame.quit()

if __name__ == "__main__":
    multiprocessing.freeze_support() # Windows에서 필수
    run_multiprocessing_simulation()