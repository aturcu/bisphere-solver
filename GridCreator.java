import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

import javafx.application.Application;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import javafx.stage.Stage;
 
/**
* This is the GridCreator class that is responsible for taking in files created by the solver_boolean 
* SAT solver and turning them into a 2D grid representation (with green circles for backbone spheres, red circles 
* for sidechain spheres, thick green lines for edges, and thin red lines for contacts).
*/
public class GridCreator extends Application {
 
	/**
	 * This launches the program.
	 * 
	 * @param args
	 */
    public static void main(String[] args) {
        launch(args);
    }
 
    /**
     * This reads information from the appropriate files and sets up 
     * the canvas on which the grid will be displayed. 
     */
    @Override
    public void start(Stage initialBoard) throws IOException {     
    	
      // dimensions of grid, y by x (num rows by num cols)
    	int[] dimensions = new int[2];
    	
      // dimensions are read from file and stored in array
    	try(BufferedReader br = new BufferedReader(new FileReader(new File("board_dimensions.txt")))) {
    		String line = br.readLine();
    		
    		String[] lineArray = line.split(", ");
    		
    		dimensions[0] = Integer.parseInt(lineArray[0]);
    		dimensions[1] = Integer.parseInt(lineArray[1]);

    	}
        
        // set up board, root, canvas, and graphics context, then draw the board, set the scene, and display it
        Stage board = new Stage();
        board.setTitle("Board");
        Group root = new Group();
        Canvas canvas = new Canvas(50*dimensions[1], 50*dimensions[0]);
        GraphicsContext gc = canvas.getGraphicsContext2D();
        drawBoard(gc, new File("backbone.txt"), new File("sidechain.txt"), new File("edges.txt"), new File("contacts.txt"),dimensions);
        root.getChildren().add(canvas);
        board.setScene(new Scene(root));
        board.show();
    }

    /**
     * This method draws the board given the dimensions of the grid, as well as where on 
     * the board we have a backbone, sidechain, edge, or contact.
     * 
     * @param gc
     * @param backbone board
     * @param sidechain board
     * @param edge board
     * @param contact board
     * @param dimensions
     * @throws IOException
     */
    private void drawBoard(GraphicsContext gc, File backbone, File sidechain, File edges, File contacts, int[] dimensions) throws IOException {

        gc.setFill(Color.BLACK);
        gc.setStroke(Color.GREEN);
        gc.setLineWidth(5);

        // reads edges file, puts edges in between appropriate backbone and sidechain spheres
        try(BufferedReader br = new BufferedReader(new FileReader(edges))) {

            int row1 = 0;
            int col1 = 0;
            int row2 = 0;
            int col2 = 1;
            boolean horizontal = true;

            for(String line; (line = br.readLine()) != null;) {
              String[] lineArray = line.split(", ");
              for(int edge = 0; edge < lineArray.length; edge++) {
                if (lineArray[edge].compareTo("True") == 0) {
                  gc.strokeLine(20+50*col1+10, 20+50*row1+10, 20+50*col2+10, 20+50*row2+10);
                }
                col1++;
                col2++;
                if (col2 > dimensions[1]-1 && horizontal) {
                    col1 = 0;
                    col2 = 0;
                    row2++;
                    horizontal = false;
                }

                if (col2 > dimensions[1]-1 && !horizontal) {
                  col1 = 0;
                  col2 = 1;
                  row1++;
                  horizontal = true;
                }
              }
            }
        }

        gc.setStroke(Color.RED);
        gc.setLineWidth(1);

        // reads contacts file, puts contacts in between adjacent sidechain spheres
        try(BufferedReader br = new BufferedReader(new FileReader(contacts))) {

            int row1 = 0;
            int col1 = 0;
            int row2 = 0;
            int col2 = 1;
            boolean horizontal = true;

            for(String line; (line = br.readLine()) != null;) {
              String[] lineArray = line.split(", ");
              for(int edge = 0; edge < lineArray.length; edge++) {
                if (lineArray[edge].compareTo("True") == 0) {
                  gc.strokeLine(20+50*col1+10, 20+50*row1+10, 20+50*col2+10, 20+50*row2+10);
                }
                col1++;
                col2++;
                if (col2 > dimensions[1]-1 && horizontal) {
                    col1 = 0;
                    col2 = 0;
                    row2++;
                    horizontal = false;
                }

                if (col2 > dimensions[1]-1 && !horizontal) {
                  col1 = 0;
                  col2 = 1;
                  row1++;
                  horizontal = true;
                }
              }
            }
        }

        // creates a grid of black points
        for(int i = 20; i < 50*dimensions[0]; i+=50) {
        		for (int j = 20; j < 50*dimensions[1]; j+=50) {
        			gc.fillOval(i, j, 20, 20);
        		}
        }
        
        gc.setFill(Color.GREEN);

        // reads backbone file, puts green spheres in appropriate locations
        try(BufferedReader br = new BufferedReader(new FileReader(backbone))) {

            int row = 0;

        		for(String line; (line = br.readLine()) != null;) {
        			String[] lineArray = line.split(", ");
              for(int col = 0; col < lineArray.length; col++) {
                if (lineArray[col].compareTo("True") == 0) {
                  gc.fillOval(20+50*col-5, 20+50*row-5, 30, 30);
                }
              }
              row++;
            }
        }

        gc.setFill(Color.RED);

        // reads sidechain file, puts red spheres in appropriate locations
        try(BufferedReader br = new BufferedReader(new FileReader(sidechain))) {

            int row = 0;

            for(String line; (line = br.readLine()) != null;) {
              String[] lineArray = line.split(", ");
              for(int col = 0; col < lineArray.length; col++) {
                if (lineArray[col].compareTo("True") == 0) {
                  gc.fillOval(20+50*col-5, 20+50*row-5, 30, 30);
                }
              }
              row++;
            }
        }
    }
}