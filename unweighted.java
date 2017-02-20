/**
 * Created by chenruqian on 2/11/17.
 * TODO: create a vertex class (list of vertices as its component member, birth time, death time, degree), and a tree class?
 */
import java.util.NoSuchElementException;
import java.util.Scanner;
import java.util.List;
import java.util.ArrayList;

public class unweighted {
    public static void main(String[] args) {

        ////////////////////////
        // INPUT format
        ////////////////////////
        // first integer: # vertices
        // second integer: # edges
        // next 2n = n pair of integers: (a,b) for edge(a,b)
        // next n integers: the i-th vertex's degree
        // next e integers: the j-th edge's weight
        // next e integers: edge indices sorted in descending order of edge weight

        ////////////////////////
        // INPUT arrays, length
        ////////////////////////
        //edgeWeight, e
        //edgePQ, e
        //inVertex, e
        //outVertex, e
        //degree, n

        /////////////////////////
        // OUTPUT arrays, length
        /////////////////////////
        // componentSize, n
        // rep, n
        // death, n // death = -1 indicating it never died


        try {
            Scanner sn = new Scanner(System.in);

            int n = sn.nextInt(); // number of vertices
            int e = sn.nextInt(); // number of edges
            int[] outVertex = new int[e];
            int[] inVertex = new int[e];
            for (int i = 0; i < e; i++) {
                outVertex[i] = sn.nextInt() - 1;
                inVertex[i] = sn.nextInt() - 1;
            }
            
            int[] degree = initialize(n, 0);
            for (int i = 0; i < n; i++) {
                degree[i] = sn.nextInt();
            }
           
            int[] edgeWeight = initialize(e, 0);
            for (int j = 0; j < e; j++) {
                edgeWeight[j] = sn.nextInt();
            }
            int[] edgePQ = initialize(e, 0);
            for (int j = 0; j < e; j++) {
                edgePQ[j] = sn.nextInt()-1;
            }

            int[] merge = initialize(n,-1);

            int[] rep = new int[n];
            for (int j = 0; j < n; j++){
                rep[j] = j;
            } // start with every vertex being its own representative
            int[] componentSize = initialize(n, 0);
            int[] death = initialize(n, -1);

            for (int k = 0; k < e; k++) {
                int j = edgePQ[k];
                int v = outVertex[j];
                int w = inVertex[j];
                int repv = rep[v];
                int repw = rep[w];
                if (rep[v]!=rep[w]) {
                    if (degree[repv] >= degree[repw]){
                        if (repw == w){
                            merge[w] = repv;
                        }
                        rep[repw] = repv;
                        death[repw] = edgeWeight[j];
                        rep[w] = repv;
                        for (int i = 0; i < n;i++){ //TODO runtime is not ideal here. Fix.
                            if (rep[i] == repw){ rep[i] = repv; }
                        }
                    }
                    else{
                        if (repv == v){
                            merge[v] = repw;
                        }
                        rep[repv] = repw;
                        death[repv] = edgeWeight[j];
                        rep[v] = repw;
                        for (int i = 0; i < n; i++){
                            if (rep[i] == repv){rep[i] = repw;}
                        }
                    }
                }
            }

            //List<List<Integer>> group = new ArrayList<>(4);

            for (int j = 0; j < n; j++) {
                componentSize[rep[j]]++;
            } // NB: the componentSize vector should sum up to n

            System.out.println("VIndex,ComponentSize,Representative,Birth,Death,Merge");
            for (int i = 0; i < n; i++) {
                int j = i+1;
                int representative = rep[i] + 1;
                int merged = merge[i];
                if (merge[i] != -1) {merged ++;}
                System.out.println(j+","+componentSize[i]+","+representative+","+ degree[i]+","+ death[i]+","+merged);
            }
        } catch(NoSuchElementException e){ e.printStackTrace(); }
    }


    public static int max(int[] arr){ // find the max in an array of positive numbers
        int count = 0;
        for (int j = 0; j < arr.length; j++){
            if (arr[j] > count){
                count = arr[j];
            }
        }
        return count;
    }
    public static int min(int[] arr){ // find the max in an array of positive numbers
        int count = arr[0];
        for (int j = 1; j < arr.length; j++){
            if (arr[j] < count){
                count = arr[j];
            }
        }
        return count;
    }
    public static int[] initialize(int n, int val){ // declare and initialize an int array of length n, with val.
        int[] ans = new int[n];
        for (int j = 0; j < n; j++){
            ans[j] = val;
        }
        return ans;
    }
}