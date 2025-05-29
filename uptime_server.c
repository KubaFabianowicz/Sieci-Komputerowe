#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/types.h>

#define DEFAULT_PORT 80
#define BUFFER_SIZE 1024

const char* http_header_template = "HTTP/1.0 200 OK\r\n"
                                   "Content-Type: text/plain; charset=UTF-8\r\n"
                                   "Connection: close\r\n"
                                   "Content-Length: %d\r\n"
                                   "\r\n";

void error_exit(const char* msg) {
    perror(msg);
    exit(EXIT_FAILURE);
}

char* get_uptime_str() {
    static char uptime[64];
    FILE* f = fopen("/proc/uptime", "r");
    if (!f) return NULL;
    if (fgets(uptime, sizeof(uptime), f) == NULL) {
        fclose(f);
        return NULL;
    }
    fclose(f);
    // Tylko pierwsza liczba
    char* space = strchr(uptime, ' ');
    if (space) *space = '\0';
    strcat(uptime, "\n");
    return uptime;
}

int main(int argc, char* argv[]) {
    int port = DEFAULT_PORT;

    if (getuid() == 0) {
        fprintf(stderr, "Nie uruchamiaj programu jako root!\n");
        return EXIT_FAILURE;
    }

    if (argc > 1) {
        port = atoi(argv[1]);
    }

    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) error_exit("socket");

    int opt = 1;
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0)
        error_exit("setsockopt");

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_ANY);  
    addr.sin_port = htons(port);

    if (bind(server_fd, (struct sockaddr*)&addr, sizeof(addr)) < 0)
        error_exit("bind");

    if (listen(server_fd, 10) < 0)
        error_exit("listen");

    printf("Serwer działa na porcie %d\n", port);

    while (1) {
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);
        int client_fd = accept(server_fd, (struct sockaddr*)&client_addr, &client_len);
        if (client_fd < 0) {
            perror("accept");
            continue;
        }

        char buffer[BUFFER_SIZE];
        int received = recv(client_fd, buffer, sizeof(buffer) - 1, 0);
        if (received <= 0) {
            close(client_fd);
            continue;
        }

        char* uptime = get_uptime_str();
        if (!uptime) {
            close(client_fd);
            continue;
        }

        char response[BUFFER_SIZE];
        int content_len = strlen(uptime);
        int header_len = snprintf(response, sizeof(response), http_header_template, content_len);
        send(client_fd, response, header_len, 0);
        send(client_fd, uptime, content_len, 0);

        shutdown(client_fd, SHUT_WR);
        close(client_fd);
        printf("Obsłużono klienta\n");
    }

    close(server_fd);
    return 0;
}

#kompilacja
#gcc -o uptime_server uptime_server.c

#uruchamianie
#./uptime_server 8080

#testowanie
# W przeglądarce: http://localhost:8080
# w terminalu: nc localhost 8080