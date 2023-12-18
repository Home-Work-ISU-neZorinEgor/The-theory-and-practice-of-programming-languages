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
        String serverAddress = "tcp://192.168.0.102:5555";

        try (ZMQ.Context context = ZMQ.context(1);
             ZMQ.Socket subscriber = context.socket(ZMQ.SUB)) {

            // Connect to the server
            subscriber.connect(serverAddress);

            // Subscribe to all messages
            subscriber.subscribe("".getBytes());

            // Prepare for saving logs to a file
            PrintWriter logWriter = new PrintWriter(new FileWriter("subscriber_logs.dat", true));

            // Regular expression for extracting digits
            // No need for a regex pattern in this modified code

            while (true) {
                // Get current date and time
                LocalDateTime currentTime = LocalDateTime.now();
                DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

                // Receive the message
                String message = new String(subscriber.recv(0), ZMQ.CHARSET);

                // Print the entire received message to the console
                System.out.println("[" + currentTime.format(formatter) + "] " + message);

                // Extract the table name and digit from the message
                String digit = message.replaceAll("\\D", ""); // Remove non-digits

                // Save logs to the file
                logWriter.println("[" + currentTime.format(formatter) + "] Message: " + message);
                logWriter.flush();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
