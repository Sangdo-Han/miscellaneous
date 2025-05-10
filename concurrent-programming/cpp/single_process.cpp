// #include <iostream>
// #include <chrono>
// #include <string>
// #include <openssl/sha.h>
// #include <openssl/evp.h>
// #include <iomanip>
// #include <sstream>
// #include "Timer.h"

// std::string zfill(int num, int len) {
//     std::string str = std::to_string(num);
//     return std::string(len - str.length(), '0') + str;
// }

// std::string bytes_to_hex(const unsigned char* bytes, size_t len) {
//     static const char hex_chars[] = "0123456789abcdef";
//     std::string hex_str(len * 2, ' ');
//     for (size_t i = 0; i < len; ++i) {
//         hex_str[2 * i] = hex_chars[(bytes[i] >> 4) & 0xF];
//         hex_str[2 * i + 1] = hex_chars[bytes[i] & 0xF];
//     }
//     return hex_str;
// }

// std::string SHA256(const std::string& str, EVP_MD_CTX* mdctx) {
//     unsigned char hash[SHA256_DIGEST_LENGTH];
//     EVP_DigestInit_ex(mdctx, EVP_sha256(), nullptr);
//     EVP_DigestUpdate(mdctx, str.c_str(), str.length());
//     EVP_DigestFinal_ex(mdctx, hash, nullptr);
//     return bytes_to_hex(hash, SHA256_DIGEST_LENGTH);
// }

// void crack_password(const std::string& originalHash, int len, int limit) {
//     EVP_MD_CTX* mdctx = EVP_MD_CTX_new();
//     for (int i = 0; i < limit; i++) {
//         std::string candidate = zfill(i, len);
//         if (SHA256(candidate, mdctx) == originalHash) {
//             std::cout << "Match found: " << candidate << " (" << i << ")\n";
//             break;
//         }
//     }
//     EVP_MD_CTX_free(mdctx);
// }

// int main() {
//     const int answer = 8309322;
//     const int len = 7;
//     const int limit = 10000000;
    
//     std::string strAnswer = zfill(answer, len);
//     EVP_MD_CTX* mdctx = EVP_MD_CTX_new();
//     std::string originalHash = SHA256(strAnswer, mdctx);
//     EVP_MD_CTX_free(mdctx);
//     std::cout << "Original Hash: " << originalHash << "\n";
    
//     Timer timer;
//     crack_password(originalHash, len, limit);
    
//     return 0;
// }
