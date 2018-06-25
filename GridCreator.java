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
    	
    	int[] dimensions = new int[2];
    	
    	try(BufferedReader br = new BufferedReader(new FileReader(new File("board_dimensions.txt")))) {
    		String line = br.readLine();
    		
    		String[] lineArray = line.split(", ");
    		
    		dimensions[0] = Integer.parseInt(lineArray[0]);
    		dimensions[1] = Integer.parseInt(lineArray[1]);

    	}
        
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
     * This method draws the board given the dimensions of the grid and 
     * the coordinates and types of BisphereSegments written in the file.
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

        // WILL CHANGE THIS LATER TO DISPLAY BOARD CLEARLY

        gc.setFill(Color.BLACK);
		    gc.setStroke(Color.GREEN);
        for(int i = 20; i < 50*dimensions[0]; i+=50) {
        		for (int j = 20; j < 50*dimensions[1]; j+=50) {
        			gc.fillOval(i, j, 20, 20);
        		}
        }
        
		
		    gc.setLineWidth(5);
        gc.setFill(Color.GREEN);
        try(BufferedReader br = new BufferedReader(new FileReader(backbone))) {

            int row = 0;

        		for(String line; (line = br.readLine()) != null;) {
        			String[] lineArray = line.split(", ");

              for(int col = 0; col < lineArray.size; i++) {
                if (lineArray[i] == "True") {
                  gc.fillOval(20+50*row-5, 20+50*col-5, 30, 30);
                }
              }
              row++;
            }
        		
  //       			for (int i = 0; i < 6; i++) {
  //       				segmentInfo[i] = Integer.parseInt(lineArray[i]);
  //       			}
        		
  //       			int[] sphere1Coords = {20+50*segmentInfo[1], 20+50*segmentInfo[0]};
  //       			int[] sphere2Coords = {20+50*segmentInfo[4], 20+50*segmentInfo[3]};
        		
  //       			gc.strokeLine(sphere1Coords[0]+10, sphere1Coords[1]+10, sphere2Coords[0]+10, sphere2Coords[1]+10);
        		
  //       			if (segmentInfo[2] == 0) {
  //       				gc.setFill(Color.GREEN);
  //       				gc.fillOval(sphere1Coords[0]-5, sphere1Coords[1]-5, 30, 30);
  //       			} else {
  //       				gc.setFill(Color.RED);
  //       				gc.fillOval(sphere1Coords[0]-5, sphere1Coords[1]-5, 30, 30);
  //       			}
        		
  //       			if (segmentInfo[5] == 0) {
  //       				gc.setFill(Color.GREEN);
  //       				gc.fillOval(sphere2Coords[0]-5, sphere2Coords[1]-5, 30, 30);
  //       			} else {
  //       				gc.setFill(Color.RED);
  //       				gc.fillOval(sphere2Coords[0]-5, sphere2Coords[1]-5, 30, 30);
  //       			}
        		}
        }
}