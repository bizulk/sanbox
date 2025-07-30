#include <iostream>
#include <cmath>
#include <chrono>
#include <thread>
#include <atomic>

using namespace std::chrono;

// Variables globales observables
// extern C évite le name mangling et simplifie l'inspection de ces variables.
extern "C" {
    double A = 1.0;
    double B = 0.0;
    double X = 0.0;
    double Y = 0.0;
    int run = 1;
}

// Fonction utilitaire pour obtenir le temps en secondes
double getCurrentTime() {
    auto now = high_resolution_clock::now();
    auto epoch = now.time_since_epoch();
    return duration_cast<duration<double>>(epoch).count();
}

int main(int argc, char * argv[]) {
    double lastPrint = 0.0;

    double startime = getCurrentTime();

    while (true) {
        // 
        if (run) {
            X = getCurrentTime() - startime;
            Y = std::cos(A * X + B);

            double now = getCurrentTime();
            if (now - lastPrint >= 0.5) {
                std::cout << "X: " << X << " | Y: " << Y << " | A: " << A << " | B: " << B << " | run: " << run << std::endl;
                lastPrint = now;
            }
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }

    return 0;
}
