#pragma once
#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <mutex>
#include <chrono>

class SGM_Engine {
private:
    std::vector<int> ref_counts; // Счетчики ссылок
    std::vector<bool> is_garbage; // Флаги мусора
    std::vector<bool> is_needed;  // Флаги "нужных" объектов
    bool running;
    std::mutex mtx;

public:
    SGM_Engine(int num_objects) : running(false) {
        ref_counts.resize(num_objects, 0);
        is_garbage.resize(num_objects, false);
        is_needed.resize(num_objects, false);
    }

    // Устанавливаем счетчик ссылок (если > 0, объект нужен)
    void set_ref(int index, int count) {
        std::lock_guard<std::mutex> lock(mtx);
        if (index >= 0 && index < static_cast<int>(ref_counts.size())) {
            ref_counts[index] = count;
            is_needed[index] = (count > 0);
        }
    }

    // Создаем цикл (A ссылается на B, B ссылается на A)
    void create_cycle(int a, int b) {
        std::lock_guard<std::mutex> lock(mtx);
        ref_counts[a] = 1;
        ref_counts[b] = 1;
        is_needed[a] = true;
        is_needed[b] = true;
    }

    // Находим мусор (включая циклы)
    void find_garbage() {
        std::lock_guard<std::mutex> lock(mtx);
        int found = 0;
        for (size_t i = 0; i < ref_counts.size(); i++) {
            // Если счетчик ссылок 0 — это мусор
            // Если счетчик > 0, но объект в цикле (и нет внешних ссылок) — тоже мусор (упрощенно)
            if (ref_counts[i] == 0 || (ref_counts[i] > 0 && !is_needed[i])) {
                is_garbage[i] = true;
                found++;
            }
        }
        std::cout << "[SGM Finder] Found " << found << " garbage objects." << std::endl;
    }

    // Удаляем мусор (с проверкой ошибки 654)
    bool delete_garbage() {
        std::lock_guard<std::mutex> lock(mtx);
        int deleted = 0;
        for (size_t i = 0; i < is_garbage.size(); i++) {
            if (is_garbage[i]) {
                // ПРОВЕРКА: Если объект "нужен" (is_needed), выдаем ошибку 654
                if (is_needed[i]) {
                    std::cout << "\033[91m[ERROR 654] Attempt to delete needed object " << i << "!\033[0m" << std::endl;
                    return false; // Ошибка!
                }
                // Удаляем
                ref_counts[i] = -1;
                is_garbage[i] = false;
                deleted++;
            }
        }
        std::cout << "[SGM Deleter] Freed " << deleted << " objects." << std::endl;
        return true; // Успех
    }

    // Автоматический запуск SGM (3-5 проходов)
    void run_auto(int passes = 3) {
        running = true;
        std::thread([this, passes]() {
            for (int p = 0; p < passes && running; p++) {
                std::cout << "\n[SGM] Pass " << (p + 1) << " of " << passes << std::endl;
                find_garbage();
                if (!delete_garbage()) {
                    std::cout << "\033[91m[SGM] Stopping due to Error 654.\033[0m" << std::endl;
                    break;
                }
                std::this_thread::sleep_for(std::chrono::milliseconds(500));
            }
            std::cout << "[SGM] Auto mode finished." << std::endl;
        }).detach();
    }

    void stop() {
        running = false;
    }
};
