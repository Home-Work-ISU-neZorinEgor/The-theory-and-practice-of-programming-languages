package org.example;

import org.zeromq.ZMQ;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Client {

    public static void main(String[] args) {
        String serverAddress = "tcp://192.168.0.102:5555";

        try (ZMQ.Context context = ZMQ.context(1);
             ZMQ.Socket subscriber = context.socket(ZMQ.SUB)) {

            // Подключение к серверу
            subscriber.connect(serverAddress);

            // Установка подписки на все сообщения
            subscriber.subscribe("".getBytes());

            // Подготовка для сохранения логов в файл
            PrintWriter logWriter = new PrintWriter(new FileWriter("subscriber_logs.dat", true));

            // Регулярное выражение для извлечения цифры
            Pattern pattern = Pattern.compile("\\d+");

            while (true) {
                // Получение текущей даты и времени
                LocalDateTime currentTime = LocalDateTime.now();
                DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

                // Получение сообщения
                String message = new String(subscriber.recv(0), ZMQ.CHARSET);

                // Извлечение цифры из сообщения
                Matcher matcher = pattern.matcher(message);
                if (matcher.find()) {
                    String digit = matcher.group();

                    // Вывод в консоль с добавлением времени
                    System.out.println("[" + currentTime.format(formatter) + "] " + digit);

                    // Запись в лог-файл с добавлением времени
                    logWriter.println("[" + currentTime.format(formatter) + "] " + digit);
                    logWriter.flush();  // Сбрасываем буфер, чтобы убедиться, что данные записаны в файл
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
