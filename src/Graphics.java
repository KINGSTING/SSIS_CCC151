package src;

import javax.swing.*;
import javax.swing.border.Border;
import javax.swing.border.TitledBorder;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Scanner;
public class Graphics {
    public Graphics() {
        JFrame fr = new JFrame();
        JPanel panel = new JPanel();
        JPanel panel2 = new JPanel();
        JPanel panel3 = new JPanel();
        JButton addButton = new JButton("Add");
        JButton clrButton = new JButton("Clear");
        JButton edtButton = new JButton("Edit");
        JButton delButton = new JButton("Delete");
        JButton savButton = new JButton("Save");

        Functions func = new Functions();

        DefaultTableModel tableModel = new DefaultTableModel();
        JTable tabs = new JTable();

        JTextField txt1 = new JTextField();
        JTextField txt2 = new JTextField();
        JTextField txt3 = new JTextField();
        JTextField txt4 = new JTextField();
        JTextField txt5 = new JTextField();
        Font myFont = new Font("Arial", Font.PLAIN, 13);


        fr.setTitle("Simple Student Information System");
        fr.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        fr.setSize(850, 650);
        fr.setResizable(false);
        fr.setLayout(null);

        //Segment #1------------------------------------------------------------------

        panel.setBounds(3, 3, 550, 330);
        panel.setLayout(new GridBagLayout());
        panel.setBackground(Color.white);

        GridBagConstraints cons = new GridBagConstraints();
        cons.insets = new Insets(5, 5, 5, 5);

        JLabel label1 = new JLabel("Name:");
        label1.setFont(myFont);
        cons.gridx = 0;
        cons.gridy = 0;
        cons.fill = GridBagConstraints.HORIZONTAL;
        panel.add(label1, cons);

        JLabel label2 = new JLabel("ID_Number:");
        label2.setFont(myFont);
        cons.gridx = 0;
        cons.gridy = 1;
        cons.fill = GridBagConstraints.HORIZONTAL;
        panel.add(label2, cons);

        JLabel label3 = new JLabel("Year_Level:");
        label3.setFont(myFont);
        cons.gridx = 0;
        cons.gridy = 2;
        cons.fill = GridBagConstraints.HORIZONTAL;
        panel.add(label3, cons);

        JLabel label4 = new JLabel("Gender:");
        label4.setFont(myFont);
        cons.gridx = 0;
        cons.gridy = 3;
        cons.fill = GridBagConstraints.HORIZONTAL;
        panel.add(label4, cons);

        JLabel label5 = new JLabel("Course_Code:");
        label5.setFont(myFont);
        cons.gridx = 0;
        cons.gridy = 4;
        cons.fill = GridBagConstraints.HORIZONTAL;
        panel.add(label5, cons);

        //txt1
        txt1.setPreferredSize(new Dimension(150, 20));
        cons.gridx = 1;
        cons.gridy = 0;
        cons.gridwidth = 5;
        cons.fill = GridBagConstraints.HORIZONTAL;
        panel.add(txt1, cons);

        //txt2
        txt2.setPreferredSize(new Dimension(150, 20));
        cons.gridx = 1;
        cons.gridy = 1;
        cons.fill = GridBagConstraints.HORIZONTAL;
        cons.gridwidth = 5;
        panel.add(txt2, cons);

        //txt3
        txt3.setPreferredSize(new Dimension(150, 20));
        cons.gridx = 1;
        cons.gridy = 2;
        cons.fill = GridBagConstraints.HORIZONTAL;
        cons.gridwidth = 5;
        panel.add(txt3, cons);

        txt4.setPreferredSize(new Dimension(150, 20));
        cons.gridx = 1;
        cons.gridy = 3;
        cons.fill = GridBagConstraints.HORIZONTAL;
        cons.gridwidth = 5;
        panel.add(txt4, cons);

        txt5.setPreferredSize(new Dimension(150, 20));
        cons.gridx = 1;
        cons.gridy = 4;
        cons.fill = GridBagConstraints.HORIZONTAL;
        cons.gridwidth = 5;
        panel.add(txt5, cons);


        Border borderline = BorderFactory.createLineBorder(Color.black);
        TitledBorder titledBorder = BorderFactory.createTitledBorder("Register Here");
        panel.setBorder(borderline);
        panel.setBorder(titledBorder);

        //Segment #2------------------------------------------------------------------

        //buttons sizes
        clrButton.setPreferredSize(new Dimension(80, 20));
        addButton.setPreferredSize(new Dimension(80, 20));
        savButton.setPreferredSize(new Dimension(80, 20));
        edtButton.setPreferredSize(new Dimension(80, 20));
        delButton.setPreferredSize(new Dimension(80, 20));
        //buttons background colors
        clrButton.setBackground(Color.white);
        addButton.setBackground(Color.white);
        savButton.setBackground(Color.white);
        edtButton.setBackground(Color.white);
        delButton.setBackground(Color.white);
        //buttons functionality
        addButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String name= txt1.getText();
                String idnum = txt2.getText();
                String yrlvl = txt3.getText();
                String gender = txt4.getText();
                String courseCode = txt5.getText();
                try {
                    if (!name.isEmpty() && !idnum.isEmpty() && !yrlvl.isEmpty() && !gender.isEmpty() && !courseCode.isEmpty()) {
                        String[] rowData = {name, idnum, yrlvl, gender, courseCode};
                        tableModel.addRow(rowData);
                        txt1.setText(" ");
                        txt2.setText(" ");
                        txt3.setText(" ");
                        txt4.setText(" ");
                        txt5.setText(" ");

                    }
                } catch (NumberFormatException ex) {
                    JOptionPane.showMessageDialog(panel, "Invalid input. Please enter an integer.", "Error", JOptionPane.ERROR_MESSAGE);
                }
            }
        });
        clrButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                txt1.setText(" ");
                txt2.setText(" ");
                txt3.setText(" ");
            }
        });
        savButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                addButton.setEnabled(true);
                String name = txt1.getText();
                String idnum = txt2.getText();
                String yrlvl = txt3.getText();
                String gender = txt4.getText();
                String courseCode = txt5.getText();
                try {
                    int selectedRow = tabs.getSelectedRow();
                    if (!name.isEmpty() && !idnum.isEmpty() && !yrlvl.isEmpty() && !gender.isEmpty() && !courseCode.isEmpty()) {
                        if (selectedRow != -1) {
                            tableModel.setValueAt(name, selectedRow, 0);
                            tableModel.setValueAt(idnum, selectedRow, 1);
                            tableModel.setValueAt(yrlvl, selectedRow, 2);
                            tableModel.setValueAt(gender, selectedRow, 3);
                            tableModel.setValueAt(courseCode, selectedRow, 4);

                            txt1.setText("");
                            txt2.setText("");
                            txt3.setText("");
                            txt4.setText("");
                            txt5.setText("");
                        }
                    }
                } catch (NumberFormatException ex) {
                    JOptionPane.showMessageDialog(panel, "Somethings is wrong, please check the inputs.", "Error", JOptionPane.ERROR_MESSAGE);
                    addButton.setEnabled(false);
                }
            }
        });
        delButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                int selectedRow = tabs.getSelectedRow();
                if (selectedRow != -1) {
                    tableModel.removeRow(selectedRow);
                }
            }
        });
        edtButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                addButton.setEnabled(false);
                int selectedRow = tabs.getSelectedRow();
                if (selectedRow != -1) {
                    Object name = tabs.getValueAt(selectedRow, 0);
                    Object idnum = tabs.getValueAt(selectedRow, 1);
                    Object yrlvl = tabs.getValueAt(selectedRow, 2);
                    Object gender = tabs.getValueAt(selectedRow, 3);
                    Object courseCode= tabs.getValueAt(selectedRow, 4);
                    txt1.setText(name.toString());
                    txt2.setText(idnum.toString());
                    txt3.setText(yrlvl.toString());
                    txt4.setText(gender.toString());
                    txt5.setText(courseCode.toString());
                }
            }
        });

        panel2.setBounds(555, 3, 170, 230);
        panel2.setBackground(Color.white);
        panel2.setLayout(new GridBagLayout());
        cons.insets = new Insets(10, 10, 10, 10);
        cons.anchor = GridBagConstraints.CENTER; // Center horizontally
        cons.gridx = 0; // Column 0
        cons.gridy = GridBagConstraints.RELATIVE; // Start at the first row

        panel2.add(addButton, cons);
        panel2.add(edtButton, cons);
        panel2.add(delButton, cons);
        panel2.add(savButton, cons);
        panel2.add(clrButton, cons);

        //Segment #3-----------------------------------------------------------------

        panel3.setBounds(3, 335, 627, 180);
        panel3.setBackground(Color.white);
        tableModel.addColumn("Name");
        tableModel.addColumn("ID_Number");
        tableModel.addColumn("Year_Level");
        tableModel.addColumn("Gender");
        tableModel.addColumn("Course_Code");
        tabs.setModel(tableModel);
        tabs.setEnabled(true);
        tabs.setBackground(Color.white);

        JScrollPane scrollPane = new JScrollPane(tabs);
        scrollPane.setPreferredSize(new Dimension(627, 170));
        scrollPane.setBackground(Color.white);
        panel3.add(scrollPane);


        fr.getContentPane().add(panel);
        fr.getContentPane().add(panel2);
        fr.getContentPane().add(panel3);
        fr.setVisible(true);

    }
}
