#pragma once
#include <iostream>
#include <string>
#include <chrono>
#include <mutex>

class BRequests {
private:
    std::string target_library;
    int max_requests_per_minute;
    int current_requests;
    std::chrono::steady_clock::time_point last_reset;
    std::mutex mtx;

public:
    BRequests() : max_requests_per_minute(10), current_requests(0) {
        last_reset = std::chrono::steady_clock::now();
    }

    void check_to(const std::string& lib_name) {
        target_library = lib_name;
        std::cout << "[BRequests] Monitoring library: " << target_library << std::endl;
    }

    void settings(int times_per_minute) {
        max_requests_per_minute = times_per_minute;
        std::cout << "[BRequests] Rate limit set to: " << max_requests_per_minute << " req/min" << std::endl;
    }

    bool run() {
        std::lock_guard<std::mutex> lock(mtx);
        auto now = std::chrono::steady_clock::now();
        auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(now - last_reset).count();

        // Сбрасываем счетчик каждую минуту
        if (elapsed >= 60) {
            current_requests = 0;
            last_reset = now;
        }

        current_requests++;
        
        if (current_requests > max_requests_per_minute) {
            std::cout << "[BRequests] RATE LIMIT EXCEEDED! Blocking request." << std::endl;
            return false; // Блокируем
        }
        
        return true; // Пропускаем
    }
};
