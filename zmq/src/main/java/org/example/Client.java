package org.example;

import org.zeromq.ZMQ;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Map;

public class Client {


    public static void main(String[] args) {
        String serverAddress = "tcp://192.168.0.104:5555";

        try (ZMQ.Context context = ZMQ.context(1);
             ZMQ.Socket subscriber = context.socket(ZMQ.SUB)) {

            subscriber.connect(serverAddress);

            subscriber.subscribe("".getBytes());

            PrintWriter logWriter = new PrintWriter(new FileWriter("subscriber_logs.dat", true));


            while (true) {
                LocalDateTime currentTime = LocalDateTime.now();
                DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

                String message = new String(subscriber.recv(0), ZMQ.CHARSET);

                System.out.println("[" + currentTime.format(formatter) + "] " + message);

                String digit = message.replaceAll("\\D", ""); // Remove non-digits

                logWriter.println("[" + currentTime.format(formatter) + "] Message: " + message);
                logWriter.flush();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
