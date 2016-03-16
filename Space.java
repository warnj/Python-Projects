/*
This program will space a doucument appropriatly: 2 spaces after a period, otherwise 1
space between tokens.

STILL NEEDS TO BE VERIFIED THAT THIS WORKS
*/

import java.util.*;
import java.io.*;

public class Space {
      
   public static void main (String[] args) throws FileNotFoundException {
      Scanner console = new Scanner(System.in);
      System.out.print("input file name? ");
      //Scanner input = new Scanner(new File(console.next()));
      Scanner input = new Scanner("testessay.txt");
      System.out.print("output file name? ");
      //PrintStream output = new PrintStream(new File(console.next()));
      PrintStream output = new PrintStream("output.txt");
      space(input, output);
   }
      
    public static void space (Scanner input, PrintStream output) {
      while (input.hasNextLine()) {
         String line = input.nextLine();
         Scanner s = new Scanner(line);
         while (s.hasNext()) {
            String token = s.next();
            output.print(token + " ");
            if(token.endsWith(".")) {
               output.print(" ");
            }
         }
         output.println();
      }
   }
}