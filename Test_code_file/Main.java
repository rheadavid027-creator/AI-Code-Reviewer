
import java.util.Arrays;
class Main {
   public static void main (String arg[])
   {
      int [] arr = {1,2,3,4,5};      
      for (int i = arr.length - 1 ; i >  0; i--) {
         arr[i] = arr[i - 1];
      }
      System.out.println(Arrays.toString(arr));
   }   
}