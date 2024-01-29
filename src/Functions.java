package src;

import javax.swing.table.DefaultTableModel;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;


public class Functions extends Graphics {
    private static String e;
    static StringBuilder sb = new StringBuilder();
    static Scanner scan = new Scanner(System.in);
    static String sourceFilePath = "C:\\Users\\Jemar John\\Documents\\CCC151_CSV\\Course.csv";
    static String destinationFilePath = "C:\\Users\\Jemar John\\Documents\\CCC151_CSV\\Student.csv";


    public static void main(String[] args) {
        Functions m = new Functions();

    }

    // Modify studentCSV to accept data and file path
    public static void studentCSV(DefaultTableModel tableModel, String filePath) {
        StringBuilder sb = new StringBuilder();
        sb.append("Name:").append(",").append("ID_#:").append(",").append("Yr_Lvl:").append(",").append("Course_Code:").append("\n");

        int rowCount = tableModel.getRowCount();
        for (int i = 0; i < rowCount; i++) {
            for (int j = 0; j < tableModel.getColumnCount(); j++) {
                sb.append(tableModel.getValueAt(i, j)).append(",");
            }
            sb.append("\n");
        }

        try (FileWriter writer = new FileWriter(filePath)) {
            writer.write(sb.toString());
            System.out.println("Student CSV created!");
        } catch (IOException e) {
            System.err.println("Error creating student CSV: " + e.getMessage());
        }
    }

    // Modify courseCSV to accept data and file path
    public static void courseCSV(DefaultTableModel tableModel, String filePath) {
        StringBuilder sb = new StringBuilder();
        sb.append("Name:").append(",").append("ID_#:").append(",").append("Yr_Lvl:").append(",").append("Course_Code:").append("\n");

        int rowCount = tableModel.getRowCount();
        for (int i = 0; i < rowCount; i++) {
            for (int j = 0; j < tableModel.getColumnCount(); j++) {
                sb.append(tableModel.getValueAt(i, j)).append(",");
            }
            sb.append("\n");
        }

        try (FileWriter writer = new FileWriter(filePath)) {
            writer.write(sb.toString());
            System.out.println("Course CSV created!");
        } catch (IOException e) {
            System.err.println("Error creating course CSV: " + e.getMessage());
        }
    }

    public static void CSV2CSV() {
        try {
            BufferedReader csvReader = new BufferedReader(new FileReader(sourceFilePath));

            FileWriter csvWriter = new FileWriter(destinationFilePath);

            // Read the header from the source file and write it to the destination file
            String header = csvReader.readLine();
            csvWriter.append(header).append("\n");

            // Read and copy each line from the source to the destination file
            String line;
            while ((line = csvReader.readLine()) != null) {
                csvWriter.append(line).append("\n");
            }

            // Close the BufferedReader and FileWriter
            csvReader.close();
            csvWriter.close();

            System.out.println("Data copied from " + sourceFilePath + " to " + destinationFilePath);

        } catch (IOException e) {
            System.err.println("Error copying data: " + e.getMessage());
        }
    }
}
