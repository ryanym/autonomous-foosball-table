/*#include "opencv2/highgui/highgui.hpp"
#include <iostream>

using namespace cv;
using namespace std;

int main()
{
	Mat image;
	VideoCapture cap;
	cap.open(0);
	namedWindow("window", 1);
	while (1) {
		cap >> image;
		imshow("window", image);
		waitKey(100);
	}

} */


/*
#include <opencv\cvaux.h>
#include <opencv\highgui.h>
#include <opencv\cxcore.h>

#include <stdio.h>
#include <stdlib.h>
int times = 0;
///////////////////////////////
int main(int argc, char* argv[]) {
	float previous[3] = {0,0,0};
	float predict[3] = {0,0,0 };
	CvSize size1280x720 = cvSize(640, 480);

	CvCapture* p_capWeb;	//pointer for webvideo

	IplImage* p_imgOriginal; //pointer to an img structure

	IplImage* p_imgProcess;	//for image process, IPL means image process library

	CvMemStorage* p_strStorage; //necessary storage variable to pass into cvHoughCircle 

	CvSeq* p_seqCircle; //pointer to an OpenCV sequence, will be returned by cvHough Circle()

	float* p_fltXYRadius; //will be pointer to 3 element array [0]-->X [1]-->Y [2]-->Radius

	char charforKey;

	p_capWeb = cvCaptureFromCAM(0);

	if (p_capWeb == NULL) {

		printf("error: capture is null");
		getchar();
		return -1;
	}

	cvNamedWindow("orignial", CV_WINDOW_AUTOSIZE); // original size of cam

	cvNamedWindow("process", CV_WINDOW_AUTOSIZE);

	p_imgProcess = cvCreateImage(size1280x720,
		IPL_DEPTH_8U,
		1); //8-bit color depth , '1' mean 1 channel (grayscale) if it is color image use 3

	while (1) {

		p_imgOriginal = cvQueryFrame(p_capWeb); //get frame from webcam

		if (p_imgOriginal == NULL) {

			printf("error: frame is null");
			getchar();
			return -1;
		}

		cvInRangeS(p_imgOriginal, CV_RGB(0, 0, 100), CV_RGB(50, 80, 120), p_imgProcess); // min filter value and max filter value

		p_strStorage = cvCreateMemStorage(0); //allocate necessary memory storage to pass into cvHough Circle();
											  //smooth the processed image
		cvSmooth(p_imgProcess, //input
			p_imgProcess, //output
			CV_GAUSSIAN, //use Gaussian filter (average nearby pixel,with closed pixel)
			9,			//smooth filter windo width
			9);		//smooth filter windwo height
					//fill sequential structure with all circles in process image
		p_seqCircle = cvHoughCircles(p_imgProcess, //input (no colored)
			p_strStorage, //provide funtion with memory storage
			CV_HOUGH_GRADIENT, //algorthim for detect circles,only choice avaiable
			2, //size of image/2 = 'accumulator resolution' accum = res = size of img /2
			p_imgProcess->height / 4, //min distance in pixels between center of detected circle
			100,  //high threhold of canny edge detector, called by cvHoughCircle
			50,	  //low threhold of canny edge detector, called by cvHoughCircle
			10,	  // min circle radius, in pixels
			400); // max circle radius, in pixels

		for (int i = 0; i < p_seqCircle->total; i++) { //for each element in seq circle structure
			p_fltXYRadius = (float*)cvGetSeqElem(p_seqCircle, i);
			printf("position detect x=%f, y=%f, r=%f \n", p_fltXYRadius[0], p_fltXYRadius[1], p_fltXYRadius[2]);

			times++;
			if (times == 15) {
				if (!previous[0] && !previous[1] && !previous[2]) {

					previous[0] = p_fltXYRadius[0];
					previous[1] = p_fltXYRadius[1];
					previous[2] = p_fltXYRadius[2];
					times = 0;

				}
				else {

					predict[0] = p_fltXYRadius[0] + (p_fltXYRadius[0] - previous[0]);
					predict[1] = p_fltXYRadius[1] + (p_fltXYRadius[1] - previous[1]);
					predict[2] = p_fltXYRadius[2] + (p_fltXYRadius[2] - previous[2]);
					previous[0] = p_fltXYRadius[0];
					previous[1] = p_fltXYRadius[1];
					previous[2] = p_fltXYRadius[2];
					times = 0;

				}
			}
			
			//draw small green circle for object

			cvCircle(p_imgOriginal, //draw on original img
				cvPoint(cvRound(p_fltXYRadius[0]), cvRound(p_fltXYRadius[1])),//center of circle
				3, //3 pixels radius
				CV_RGB(0, 255, 0), //draw green
				CV_FILLED		//thickness, fill in circle
				);

			cvCircle(p_imgOriginal, //draw on original img
				cvPoint(cvRound(p_fltXYRadius[0]), cvRound(p_fltXYRadius[1])),//center of circle
				cvRound(p_fltXYRadius[2]), //3 pixels radius
				CV_RGB(255, 0, 0), //draw green
				3		//thickness, fill in circle
				);
			///////////////////////////////for caculation//////////////////////
			cvCircle(p_imgOriginal, //draw on original img
				cvPoint(cvRound(predict[0]), cvRound(predict[1])),//center of circle
				cvRound(predict[2]), //3 pixels radius
				CV_RGB(208, 220, 34), //draw green
				3		//thickness, fill in circle
				);

			cvCircle(p_imgOriginal, //draw on original img
				cvPoint(cvRound(predict[0]), cvRound(predict[1])),//center of circle
				3, //3 pixels radius
				CV_RGB(34, 220, 189), //draw green
				3		//thickness, fill in circle
				);


		} // end loop

		cvShowImage("Original", p_imgOriginal);
		cvShowImage("Process", p_imgProcess);

		cvReleaseMemStorage(&p_strStorage); //deallocate necessary storage to passin cvHouCircles


		charforKey = cvWaitKey(10);

		if (charforKey == 27) break; //27 means ESC



	}//end while


	cvReleaseCapture(&p_capWeb);

	cvDestroyWindow("Original");
	cvDestroyWindow("Process");
	return 0;


}

*/




////////////////////////objectdetect////////////////////////

/*

#include "opencv2\core\core.hpp"
#include "opencv2\objdetect\objdetect.hpp"
#include "opencv2\highgui\highgui.hpp"
#include "opencv2\imgproc\imgproc.hpp"
#include <iostream>

using namespace std;
using namespace cv;
CascadeClassifier cascade;
int main(int argc,char *argv[]) {

	if (!cascade.load("D:\\OpenCV\\opencv\\sources\\data\\hogcascades\\hogcascade_pedestrians.xml")) return -1;
	
	if (cascade.empty()) return -1;
	VideoCapture vid("D:\\OpenCV\\opencv\\sources\\samples\\data\\768x576.avi");
	
	if (!vid.isOpened()) {
		cout << "Error. the video cannot be opened." << endl;
		return -1;
	}

	namedWindow("Pedestrian", CV_WINDOW_AUTOSIZE);
	waitKey(1000);
	Mat frame(320, 240, CV_8U, Scalar(255));
	while (1) {
		if (!vid.read(frame)) break;
		Mat frame_gray;
		if (frame.channels() > 1) {

			cvtColor(frame, frame_gray, CV_BGR2GRAY);
			equalizeHist(frame_gray, frame_gray);
		}
		else {
			frame_gray = frame;
		}

		vector<Rect> pedestrians;
		
		cascade.detectMultiScale(
			frame_gray,pedestrians,1.1,2,0,Size(0,0),Size(30,30)
			);

		for (size_t i = 0; i < pedestrians.size(); i++) {
			Point center(pedestrians[i].x + pedestrians[i].width*0.5, pedestrians[i].y + pedestrians[i].height*0.5);
			ellipse(frame, center, Size(pedestrians[i].width*0.5, pedestrians[i].height*0.5), 0, 0, 360, Scalar(255, 0, 255), 4, 8, 0);
		}
		imshow("Pedestrian", frame);
		if (waitKey(30) >= 0) break;
	}
	return 0;
}

*/

//
//#include <opencv2/core/core.hpp>
//#include <opencv2/highgui/highgui.hpp>
//#include <opencv2/imgproc/imgproc.hpp>
//#include <iostream>
//
//using namespace cv;
//using namespace std;
//
//void createTrackbars(string);
//int R_MAX = 179;
//int G_MAX = 255;
//int B_MAX = 255;
//int R_MIN = 0;
//int G_MIN = 0;
//int B_MIN = 0;
//int Radius_MIN = 0;
//int Radius_MAX = 0;
//
//
//void on_trackbar(int, void*)
//{//This function gets called whenever a
// // trackbar position is changed
//
//
//}
//
//
//void createTrackbars(string trackbarWindowName) {
//	//create window for trackbars
//
//
//	namedWindow(trackbarWindowName, 0);
//	//create memory to store trackbar name on window
//	char TrackbarName[50];
//	sprintf(TrackbarName, "H_MIN", R_MIN);
//	sprintf(TrackbarName, "H_MAX", R_MAX);
//	sprintf(TrackbarName, "S_MIN", G_MIN);
//	sprintf(TrackbarName, "S_MAX", G_MAX);
//	sprintf(TrackbarName, "V_MIN", B_MIN);
//	sprintf(TrackbarName, "V_MAX", B_MAX);
//	//create trackbars and insert them into window
//	//3 parameters are: the address of the variable that is changing when the trackbar is moved(eg.H_LOW),
//	//the max value the trackbar can move (eg. H_HIGH), 
//	//and the function that is called whenever the trackbar is moved(eg. on_trackbar)
//	//                                  ---->    ---->     ---->      
//	createTrackbar("R_MIN", trackbarWindowName, &R_MIN, R_MAX, on_trackbar);
//	createTrackbar("R_MAX", trackbarWindowName, &R_MAX, R_MAX, on_trackbar);
//	createTrackbar("G_MIN", trackbarWindowName, &G_MIN, G_MAX, on_trackbar);
//	createTrackbar("G_MAX", trackbarWindowName, &G_MAX, G_MAX, on_trackbar);
//	createTrackbar("B_MIN", trackbarWindowName, &B_MIN, B_MAX, on_trackbar);
//	createTrackbar("B_MAX", trackbarWindowName, &B_MAX, B_MAX, on_trackbar);
//	createTrackbar("Radius_MIN", trackbarWindowName, &Radius_MIN, Radius_MIN, on_trackbar);
//	createTrackbar("Radius_MAX", trackbarWindowName, &Radius_MAX, Radius_MAX, on_trackbar);
//
//
//}
//
//int main() {
//
//	float previous[3] = { 0,0,0 };
//	float predict[3] = { 0,0,0 };
//	VideoCapture capWeb(1);
//	capWeb.set(CV_CAP_PROP_FRAME_WIDTH, 320);
//	capWeb.set(CV_CAP_PROP_FRAME_HEIGHT, 240);
//	if (capWeb.isOpened() == false) {
//
//		cout << "error: no webcam";
//		return 1;
//	}
//
//	Mat matOriginal(320, 240, CV_8U, Scalar(255)); //matrix object used in opencv2, input image for webcam
//
//	Mat matProcess; //process image
//	Mat HSV;
//	vector<Vec3f> vecCircle; //3 element for each circle
//
//	vector<Vec3f>::iterator itCircle;
//	cvNamedWindow("Control");
//	namedWindow("Original");
//	namedWindow("Processed");
//	createTrackbars("Control");
//	char keyPress = 0;
//
//	while (keyPress != 27) {
//
//		if (capWeb.read(matOriginal) == NULL) {
//
//			cout << "error: no img read";
//			break;
//
//		}
//		cvtColor(matOriginal, HSV, COLOR_RGB2HSV);
//		inRange(HSV,
//			Scalar(R_MIN, G_MIN, B_MIN),
//			Scalar(R_MAX, G_MAX, B_MAX),
//			matProcess);
//		//GaussianBlur(matProcess,
//		//	matProcess,
//		//	Size(9, 9), //smoothing window width and height in pixels
//		//	1.5);	//sigma value, determine how much the image will be blurred
//		//			//
//		//			HoughCircles(matProcess,
//		//			vecCircle,
//		//			CV_HOUGH_GRADIENT, //two-pass alogorthim for detecting circle
//		//			2,			//size of image
//		//			matProcess.rows / 4,
//		//			100,
//		//			50,
//		//			20, //min radius
//		//			500); //max radius
//		//			itCircle = vecCircle.begin();
//
//		//			int i = 0;
//		//			for (itCircle = vecCircle.begin(); itCircle != vecCircle.end(); itCircle++) {
//		//			if (i == 1) break;
//		//			i++;
//		//			float x = (*itCircle)[0];
//		//			float y = (*itCircle)[1];
//		//			float r = (*itCircle)[2];
//		//			cout << "ball position x = " << x
//		//			<< ", y = " << y
//		//			<< ", r = " << r << "\n";
//		//			if (!previous[0] && !previous[1] && !previous[2]) {
//
//		//			previous[0] = x;
//		//			previous[1] = y;
//		//			previous[2] = r;
//
//
//		//			}
//		//			else {
//
//		//			predict[0] = x + (x - previous[0]);
//		//			predict[1] = y + (y - previous[1]);
//		//			predict[2] = r;
//		//			previous[0] = x;
//		//			previous[1] = y;
//		//			previous[2] = r;
//
//
//		//			}
//
//		//			circle(matOriginal,
//		//			Point((int)(*itCircle)[0], (int)(*itCircle)[1]),
//		//			3,
//		//			Scalar(0, 255, 0), //draw green
//		//			CV_FILLED);
//
//		//			circle(matOriginal,
//		//			Point((int)(*itCircle)[0], (int)(*itCircle)[1]),
//		//			(int)(*itCircle)[2],
//		//			Scalar(0, 0, 255), //draw green
//		//			3);
//
//		//			circle(matOriginal,
//		//			Point((int)predict[0], (int)predict[1]),
//		//			(int)predict[2],
//		//			Scalar(0, 255, 0), //draw green
//		//			3);
//
//
//		//			}//end for
//
//
//		imshow("Original", HSV);
//		imshow("Process", matProcess);
//		imshow("Control",matProcess);
//
//		keyPress = waitKey(33);
//
//
//	}//end while
//
//	return 0;
//
//
//
//
//}


///*This is line and connor detection*/
//#include "opencv2/highgui/highgui.hpp"
//#include "opencv2/imgproc/imgproc.hpp"
//#include <iostream>
//#include <stdio.h>
//
//using namespace cv;
//using namespace std;
//
//Point2f center(0,0);
//
//Point2f computeIntersect(Vec4i a,Vec4i b)
//{
//    int x1 = a[0], y1 = a[1], x2 = a[2], y2 = a[3], x3 = b[0], y3 = b[1], x4 = b[2], y4 = b[3];
//
//    if (float d = ((float)(x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4)))
//    {
//        Point2f pt;
//        pt.x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / d;
//        pt.y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / d;
//        return pt;
//    }
//    else
//        return Point2f(-1, -1);
//}
//
//void sortCorners(vector<Point2f>& corners, Point2f center)
//{
//    vector<Point2f> top, bot;
//
//    for (int i = 0; i < corners.size(); i++)
//    {
//        if (corners[i].y < center.y)
//            top.push_back(corners[i]);
//        else
//            bot.push_back(corners[i]);
//    }
//
//    Point2f tl = top[0].x > top[1].x ? top[1] : top[0];
//    Point2f tr = top[0].x > top[1].x ? top[0] : top[1];
//    Point2f bl = bot[0].x > bot[1].x ? bot[1] : bot[0];
//    Point2f br = bot[0].x > bot[1].x ? bot[0] : bot[1];
//
//    corners.clear();
//    corners.push_back(tl);
//    corners.push_back(tr);
//    corners.push_back(br);
//    corners.push_back(bl);
//}
//
//int main()
//{
//    Mat src = imread("try.png");
//    if (src.empty())
//        return -1;
//
//    Mat dst = src.clone();
//
//    Mat bw;
//    cvtColor(src, bw, CV_BGR2GRAY);
//
//    Canny(bw, bw, 100, 100, 3);
//    vector<Vec4i> lines;
//    HoughLinesP(bw, lines, 1, CV_PI/180, 70, 30, 10);
//
//    vector<Point2f> corners;
//    for (int i = 0; i < lines.size(); i++)
//    {
//        for (int j = i+1; j < lines.size(); j++)
//        {
//            Point2f pt = computeIntersect(lines[i], lines[j]);
//            if (pt.x >= 0 && pt.y >= 0)
//                corners.push_back(pt);
//        }
//    }
//
//    vector<Point2f> approx;
//    approxPolyDP(Mat(corners), approx, arcLength(Mat(corners), true) * 0.02, true);
//
//    if (approx.size() != 4)
//    {
//        cout << "The object is not quadrilateral!" << endl;
//        return -1;
//    }
//
//    // Get mass center
//    for (int i = 0; i < corners.size(); i++)
//        center += corners[i];
//    center *= (1. / corners.size());
//
//    sortCorners(corners, center);
//
//    // Draw lines
//    for (int i = 0; i < lines.size(); i++)
//    {
//        Vec4i v = lines[i];
//        line(dst, Point(v[0], v[1]), Point(v[2], v[3]), CV_RGB(0,255,0));
//    }
//
//    // Draw corner points
//    circle(dst, corners[0], 3, CV_RGB(255,0,0), 2);
//    circle(dst, corners[1], 3, CV_RGB(0,255,0), 2);
//    circle(dst, corners[2], 3, CV_RGB(0,0,255), 2);
//    circle(dst, corners[3], 3, CV_RGB(255,255,255), 2);
//
//    // Draw mass center
//    circle(dst, center, 3, CV_RGB(255,255,0), 2);
//
//    // Calculate corresponding points for corner points
//    Mat quad = Mat::zeros(src.rows, src.cols/2, CV_8UC3);
//
//    vector<Point2f> quad_pts;
//    quad_pts.push_back(Point2f(0, 0));
//    quad_pts.push_back(Point2f(quad.cols, 0));
//    quad_pts.push_back(Point2f(quad.cols, quad.rows));
//    quad_pts.push_back(Point2f(0, quad.rows));
//
//    // Draw correspondig points
//    circle(dst, quad_pts[0], 3, CV_RGB(255,0,0), 2);
//    circle(dst, quad_pts[1], 3, CV_RGB(0,255,0), 2);
//    circle(dst, quad_pts[2], 3, CV_RGB(0,0,255), 2);
//    circle(dst, quad_pts[3], 3, CV_RGB(255,255,255), 2);
//
//    Mat transmtx = getPerspectiveTransform(corners, quad_pts);
//    warpPerspective(src, quad, transmtx, quad.size());
//
//    // Create windows and display results
//    namedWindow("Original Image", CV_WINDOW_AUTOSIZE );
//    namedWindow("Selected Points", CV_WINDOW_AUTOSIZE );
//    namedWindow("Corrected Perspertive", CV_WINDOW_AUTOSIZE );
//
//    imshow("Original Image", src);
//    imshow("Selected Points", dst);
//    imshow("Corrected Perspertive", quad);
//
//    waitKey(); // Wait for key press
//    return 0;  // End
//}
//

#include<iostream> 
#include <opencv2/opencv.hpp> 
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <string>
using namespace cv;
using namespace std;

int main(int argc, char** argv)
{
	VideoCapture cap(1); //capture the video from web cam
	cap.set(CV_CAP_PROP_FRAME_WIDTH, 320);
	cap.set(CV_CAP_PROP_FRAME_HEIGHT, 240);
	if (!cap.isOpened())  // if not success, exit program
	{
		cout << "Cannot open the web cam" << endl;
		return -1;
	}

	namedWindow("Control", CV_WINDOW_AUTOSIZE); //create a window called "Control"

	int iLowH = 0;
	int iHighH = 179;

	int iLowS = 0;
	int iHighS = 255;

	int iLowV = 0;
	int iHighV = 255;

	//Create trackbars in "Control" window
	cvCreateTrackbar("LowH", "Control", &iLowH, 179); //Hue (0 - 179)
	cvCreateTrackbar("HighH", "Control", &iHighH, 179);

	cvCreateTrackbar("LowS", "Control", &iLowS, 255); //Saturation (0 - 255)
	cvCreateTrackbar("HighS", "Control", &iHighS, 255);

	cvCreateTrackbar("LowV", "Control", &iLowV, 255); //Value (0 - 255)
	cvCreateTrackbar("HighV", "Control", &iHighV, 255);

	while (true)
	{
		Mat imgOriginal;

		bool bSuccess = cap.read(imgOriginal); // read a new frame from video

		if (!bSuccess) //if not success, break loop
		{
			cout << "Cannot read a frame from video stream" << endl;
			break;
		}

		Mat imgHSV;

		cvtColor(imgOriginal, imgHSV, COLOR_BGR2HSV); //Convert the captured frame from BGR to HSV

		Mat imgThresholded;
		medianBlur(imgThresholded,
			imgThresholded,
						7 //smoothing window width and height in pixels
						);	//sigma value, determine how much the image will be blurred
								//
						
		inRange(imgHSV, Scalar(iLowH, iLowS, iLowV), Scalar(iHighH, iHighS, iHighV), imgThresholded); //Threshold the image

																									  //morphological opening (remove small objects from the foreground)
		//erode(imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
		dilate(imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));

		//morphological closing (fill small holes in the foreground)
		dilate(imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
		erode(imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));

		imshow("Thresholded Image", imgThresholded); //show the thresholded image
		imshow("Original", imgOriginal); //show the original image

		if (waitKey(30) == 27) //wait for 'esc' key press for 30ms. If 'esc' key is pressed, break loop
		{
			cout << "esc key is pressed by user" << endl;
			break;
		}
	}

	return 0;

}


//#include<iostream> 
//#include <opencv2/opencv.hpp> 
//#include "opencv2/highgui/highgui.hpp"
//#include "opencv2/imgproc/imgproc.hpp"
//#include <opencv2/highgui/highgui_c.h>
//#include <iostream>
//#include <string>
//using namespace cv;
//using namespace std;
//
//
//
//int main(int argc, char** argv)
//{
//	Mat M(3, 3, 0);
//
//	
//	M = (Mat_<double>(10, 10) << 75, 75, 75, 75,75, 75, 75, 75, 75,75, //row1
//		75, 75, 75, 75, 75, 75, 75, 75, 75, 75,//row2
//		75, 75, 75, 75, 75, 130, 130, 130, 75, 75, //row3
//		75, 75, 75, 75, 75, 75, 130, 75, 75, 75, //row4
//		75, 75, 130, 75, 75, 75, 130, 75, 75, 75, //row5
//		75, 75, 75, 75, 75, 75, 130, 75, 75, 75, //row6
//		75, 75, 75, 75, 75, 75, 130, 75, 75, 75, //row7
//		75, 75, 75, 130, 75, 130, 130, 130, 75, 75,//row8
//		75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 
//		75, 75, 75, 75, 75, 75, 75, 75, 75, 75);
//	
//	
//	M.assignTo(M, 0);
//	
//	cout << "M = " << endl << " " << M << endl << endl;
//	
//	medianBlur(M,
//				M,
//				3 //smoothing window width and height in pixels
//				);	//sigma value, determine how much the image will be blurred
//						//
//						
//	cout << "M = " << endl << " " << M << endl << endl;
//
//	while (true)
//	{
//		
//
//		if (waitKey(30) == 27) //wait for 'esc' key press for 30ms. If 'esc' key is pressed, break loop
//		{
//			cout << "esc key is pressed by user" << endl;
//			break;
//		}
//	}
//
//	return 0;
//
//}