package com.hackathon.continuum;

import java.util.ArrayList;
import java.util.List;
import android.os.Environment;
import java.io.OutputStream;
import android.graphics.Bitmap;
import android.os.AsyncTask;
import android.app.ActivityManager;
import java.io.*;
import java.net.URL;
import java.net.HttpURLConnection;
import java.net.URLConnection;
import android.graphics.BitmapFactory;
import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.graphics.PixelFormat;
import android.os.IBinder;
import java.io.FileOutputStream;
import android.content.ComponentName;
import android.preference.PreferenceManager;
import android.util.Log;
import android.view.Display;
import android.view.Gravity;
import android.view.MotionEvent;
import android.view.View;
import android.view.WindowManager;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ImageView;
import android.widget.ListPopupWindow;
import android.widget.PopupWindow;
import com.hackathon.continuum.R;
import com.hackathon.continuum.CustomAdapter;
import com.hackathon.continuum.PInfo;
import com.hackathon.continuum.RetrievePackages;
import java.nio.ByteBuffer;
import java.util.Random;
import android.view.animation.AnimationUtils;
import android.view.animation.Animation;

import org.json.JSONArray;
import org.json.JSONObject;

public class ServiceFloating extends Service {

    String allAPIKeys[]={"Lf3CTZJ3ZU","8HZqMTMHKH","YeUKHmWRCg","ffnWPv5Uz2"};
    int maxN=4;
    String apiKey="8HZqMTMHKH";
    String langCode="en";
	public static  int ID_NOTIFICATION = 2018;

	private WindowManager windowManager;
	private ImageView chatHead;
	private PopupWindow pwindo;

	boolean mHasDoubleClicked = false;
	long lastPressTime;
	private Boolean _enable = true;

	ArrayList<String> myArray;
	ArrayList<PInfo> apps;
	List listCity;

	@Override
	public IBinder onBind(Intent intent) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override 
	public void onCreate() {
		super.onCreate();
        Random rand=new Random();

        // nextInt is normally exclusive of the top value,
        // so add 1 to make it inclusive
        int randomNum = rand.nextInt(maxN);
        apiKey="5a64d478-9c89-43d8-88e3-c65de9999580";
		SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());

		RetrievePackages getInstalledPackages = new RetrievePackages(getApplicationContext());
		apps = getInstalledPackages.getInstalledApps(false);
		myArray = new ArrayList<String>();

		for(int i=0 ; i<apps.size() ; ++i) {
			myArray.add(apps.get(i).appname);
		}

		listCity = new ArrayList();
		for(int i=0 ; i<apps.size() ; ++i) {
			listCity.add(apps.get(i));
		}

		windowManager = (WindowManager) getSystemService(WINDOW_SERVICE);

		chatHead = new ImageView(this);
		
		chatHead.setImageResource(R.drawable.finalicon);
		
		if(prefs.getString("ICON", "floating2").equals("floating3")){
			chatHead.setImageResource(R.drawable.floating3);
		} else if(prefs.getString("ICON", "floating2").equals("floating4")){
			chatHead.setImageResource(R.drawable.floating4);
		} else if(prefs.getString("ICON", "floating2").equals("floating5")){
			chatHead.setImageResource(R.drawable.floating5);
		} else if(prefs.getString("ICON", "floating2").equals("floating5")){
			chatHead.setImageResource(R.drawable.floating2);
		}

		final WindowManager.LayoutParams params = new WindowManager.LayoutParams(
				WindowManager.LayoutParams.WRAP_CONTENT,
				WindowManager.LayoutParams.WRAP_CONTENT,
				WindowManager.LayoutParams.TYPE_PHONE,
				WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
				PixelFormat.TRANSLUCENT);

		params.gravity = Gravity.TOP | Gravity.LEFT;
		params.x = 0;
		params.y = 100;

		windowManager.addView(chatHead, params);

		try {
			chatHead.setOnTouchListener(new View.OnTouchListener() {
				private WindowManager.LayoutParams paramsF = params;
				private int initialX;
				private int initialY;
				private float initialTouchX;
				private float initialTouchY;

				@Override public boolean onTouch(View v, MotionEvent event) {
					switch (event.getAction()) {
					case MotionEvent.ACTION_DOWN:

						// Get current time in nano seconds.
						long pressTime = System.currentTimeMillis();


						// If double click...
						if (pressTime - lastPressTime <= 300) {
							//createNotification();
							ServiceFloating.this.stopSelf();
							mHasDoubleClicked = true;
						}
						else {     // If not double click....
							mHasDoubleClicked = false;
						}
						lastPressTime = pressTime; 
						initialX = paramsF.x;
						initialY = paramsF.y;
						initialTouchX = event.getRawX();
						initialTouchY = event.getRawY();
						break;
					case MotionEvent.ACTION_UP:
						break;
					case MotionEvent.ACTION_MOVE:
						paramsF.x = initialX + (int) (event.getRawX() - initialTouchX);
						paramsF.y = initialY + (int) (event.getRawY() - initialTouchY);
						windowManager.updateViewLayout(chatHead, paramsF);
						break;
					}
					return false;
				}
			});
		} catch (Exception e) {
			// TODO: handle exception
		}

		chatHead.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(View arg0) {
				//initiatePopupWindow(chatHead);
				takeScreenShot(chatHead);
                _enable = false;
				//				Intent intent = new Intent(getApplicationContext(), MainActivity.class);
				//				intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK|Intent.FLAG_ACTIVITY_SINGLE_TOP|Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
				//				getApplicationContext().startActivity(intent);
			}
		});

	}


    private void takeScreenShot(View anchor){
        Log.e("userdetailss","AM SUPER USER");
        try {
            /*
            Intent dialogIntent = new Intent(this, MainActivity.class);
            dialogIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            startActivity(dialogIntent);

            Process sh = Runtime.getRuntime().exec("su", null,null);
            OutputStream  os = sh.getOutputStream();
            os.write(("/system/bin/screencap -p " + "/storage/sdcard0/hojaoimg1.png").getBytes("ASCII"));
            os.flush();
            os.close();
            sh.waitFor();
            Bitmap screen = BitmapFactory.decodeFile("/storage/sdcard0/hojaoimg1.png");
            ByteArrayOutputStream bytes = new ByteArrayOutputStream();
            screen.compress(Bitmap.CompressFormat.JPEG, 15, bytes);
            File f = new File("/storage/sdcard0/myyhojaoimg1.jpg");
            f.createNewFile();
            FileOutputStream fo = new FileOutputStream(f);
            fo.write(bytes.toByteArray());
            fo.close();
            */

            File pix = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES);
            File screenshots = new File(pix, "Screenshots");
            File file[] = screenshots.listFiles();
            Log.d("Files", "Size: "+ file.length);
            File newestFile = null;
            for (int i=0; i < file.length; i++)
            {
                File currentFile = file[i];
                if (newestFile == null || currentFile.lastModified() > newestFile.lastModified()) {
                    newestFile = currentFile;
                }
            }
            Log.d("Newest File", "FileName:" + newestFile.getAbsolutePath());


            //Animation animation = AnimationUtils.loadAnimation(getApplicationContext(), R.anim.rotate_around_center_point);
            //chatHead.startAnimation(animation);
            /*

            Ion.with(chatHead)
                    .placeholder(R.drawable.finalicon)
                    .error(R.drawable.finalicon)
                    .animateLoad(R.anim.rotate_around_center_point)
                    .animateIn(R.anim.fadeinanimation)
                    .load("http://s10.postimg.org/bpnn04pol/reload.gif");
            */
            //chatHead.setImageResource(R.drawable.loading);
            new AsyncHttpTask().execute(newestFile.getName());
            /*
            Intent intent = new Intent(getApplicationContext(), ShowMe.class);
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            intent.putExtra("RESPONSE", response);
            startActivity(intent);
*/
        }catch(Exception e){
            Log.e("exceptionss",e.toString());
        }
    }

    public  void setChatHead(){
        chatHead.setImageResource(R.drawable.finalicon);
    }
    private static void savePic(Bitmap b, String strFileName)
    {
        FileOutputStream fos = null;
        try
        {
            fos = new FileOutputStream(strFileName);
            if (null != fos)
            {
                b.compress(Bitmap.CompressFormat.PNG, 90, fos);
                fos.flush();
                fos.close();
            }
        }
        catch (FileNotFoundException e)
        {
            e.printStackTrace();
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }

	private void initiatePopupWindow(View anchor) {
		try {
			Display display = ((WindowManager) getSystemService(Context.WINDOW_SERVICE)).getDefaultDisplay();
			ListPopupWindow popup = new ListPopupWindow(this);
			popup.setAnchorView(anchor);
			popup.setWidth((int) (display.getWidth()/(1.5)));
			//ArrayAdapter<String> arrayAdapter = 
			//new ArrayAdapter<String>(this,R.layout.list_item, myArray);
			popup.setAdapter(new CustomAdapter(getApplicationContext(), R.layout.row, listCity));
			popup.setOnItemClickListener(new OnItemClickListener() {

				@Override
				public void onItemClick(AdapterView<?> arg0, View view, int position, long id3) {
					//Log.w("tag", "package : "+apps.get(position).pname.toString());
					Intent i;
					PackageManager manager = getPackageManager();
					try {
						i = manager.getLaunchIntentForPackage(apps.get(position).pname.toString());
						if (i == null)
							throw new PackageManager.NameNotFoundException();
						i.addCategory(Intent.CATEGORY_LAUNCHER);
						startActivity(i);
					} catch (PackageManager.NameNotFoundException e) {

					}
				}
			});
			popup.show();

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public void createNotification(){
		Intent notificationIntent = new Intent(getApplicationContext(), ServiceFloating.class);
		PendingIntent pendingIntent = PendingIntent.getService(getApplicationContext(), 0, notificationIntent, 0);

		Notification notification = new Notification(R.drawable.floating2, "Click to start launcher",System.currentTimeMillis());
	    //notification.setLatestEventInfo(getApplicationContext(), "Start launcher" ,  "Click to start launcher", pendingIntent);
		notification.flags = Notification.FLAG_AUTO_CANCEL | Notification.FLAG_ONGOING_EVENT;

		NotificationManager notificationManager = (NotificationManager) getApplicationContext().getSystemService(Context.NOTIFICATION_SERVICE);

		notificationManager.notify(ID_NOTIFICATION,notification);
	}

	@Override
	public void onDestroy() {
		super.onDestroy();
		if (chatHead != null) windowManager.removeView(chatHead);
	}

    public class AsyncHttpTask extends AsyncTask<String, Void, String> {


        @Override
        protected void onPostExecute(String filteredResponse) {
            //setChatHead();

            Intent intent = new Intent(getApplicationContext(), ShowMe.class);
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            Log.d("FILTERED", "FILTERED" + filteredResponse);
            intent.putExtra("RESPONSE", filteredResponse);
            startActivity(intent);


        }

        @Override
        public String doInBackground(String... params) {

            String newestFile = params[0];
            String pathToOurFile = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES) + File.separator + "Screenshots" + File.separator + newestFile;
            Log.d("Newest File path", "FileName:" + pathToOurFile);
            HttpURLConnection connection = null;
            DataOutputStream outputStream = null;
            DataInputStream inputStream = null;

            //String urlServer = "http://api.ocrapiservice.com/1.0/rest/ocr";
            String urlServer = "https://api.ocr.space/parse/image";
            //String urlServer="http://www.google.com";
            String lineEnd = "\r\n";
            String twoHyphens = "--";
            String boundary =  "*****";

            int bytesRead, bytesAvailable, bufferSize;
            byte[] buffer;
            int maxBufferSize = 1*1024*1024;
            String filteredResponse=null;
            try
            {
                FileInputStream fileInputStream = new FileInputStream(new File(pathToOurFile));
                URL url = new URL(urlServer);
                connection = (HttpURLConnection) url.openConnection();
                connection.setDoInput(true);
                connection.setDoOutput(true);
                connection.setUseCaches(false);
                connection.setRequestMethod("POST");

                connection.setRequestProperty("Connection", "Keep-Alive");
                connection.setRequestProperty("Content-Type", "multipart/form-data;boundary="+boundary);
                //connection.setRequestProperty("apikey",apiKey);
                //connection.setRequestProperty("language",langCode);

                outputStream = new DataOutputStream( connection.getOutputStream() );

                /*
                //PARAMETER1
                outputStream.writeBytes(twoHyphens + boundary + lineEnd);
                outputStream.writeBytes("Content-Disposition: form-data; name=\"MAX_FULL_SIZE\""+lineEnd);
                outputStream.writeBytes(lineEnd);
                outputStream.writeBytes("100000000"+lineEnd);

                //PARAMETER2
                outputStream.writeBytes(twoHyphens + boundary + lineEnd);
                outputStream.writeBytes("Content-Disposition: form-data; name=\"image\";filename=\"" + newestFile +"\"" + lineEnd);
                outputStream.writeBytes("Content-Type: image/png"+lineEnd);
                outputStream.writeBytes(lineEnd);
                bytesAvailable = fileInputStream.available();
                bufferSize = Math.min(bytesAvailable, maxBufferSize);
                buffer = new byte[bufferSize];

                // Read file
                bytesRead = fileInputStream.read(buffer, 0, bufferSize);

                while (bytesRead > 0)
                {
                    outputStream.write(buffer, 0, bufferSize);
                    bytesAvailable = fileInputStream.available();
                    bufferSize = Math.min(bytesAvailable, maxBufferSize);
                    bytesRead = fileInputStream.read(buffer, 0, bufferSize);
                }
                outputStream.writeBytes(lineEnd);

                //PARAMETER3
                outputStream.writeBytes(twoHyphens + boundary + lineEnd);
                outputStream.writeBytes("Content-Disposition: form-data; name=\"language\""+lineEnd);
                outputStream.writeBytes(lineEnd);
                outputStream.writeBytes("en"+lineEnd);

                //PARAMETER4
                outputStream.writeBytes(twoHyphens + boundary + lineEnd);
                outputStream.writeBytes("Content-Disposition: form-data; name=\"apikey\""+lineEnd);
                outputStream.writeBytes(lineEnd);
                outputStream.writeBytes(apiKey+lineEnd);

                //END PARAMETER
                outputStream.writeBytes(twoHyphens + boundary + lineEnd);
                */




                //PARAMETER1
                outputStream.writeBytes(twoHyphens + boundary + lineEnd);
                outputStream.writeBytes("Content-Disposition: form-data; name=\"file\";filename=\"" + newestFile +"\"" + lineEnd);
                outputStream.writeBytes("Content-Type: image/png"+lineEnd);
                outputStream.writeBytes(lineEnd);
                bytesAvailable = fileInputStream.available();
                bufferSize = Math.min(bytesAvailable, maxBufferSize);
                buffer = new byte[bufferSize];

                // Read file
                bytesRead = fileInputStream.read(buffer, 0, bufferSize);

                while (bytesRead > 0)
                {
                    outputStream.write(buffer, 0, bufferSize);
                    bytesAvailable = fileInputStream.available();
                    bufferSize = Math.min(bytesAvailable, maxBufferSize);
                    bytesRead = fileInputStream.read(buffer, 0, bufferSize);
                }
                outputStream.writeBytes(lineEnd);

                /*
                //PARAMETER2
                outputStream.writeBytes(twoHyphens + boundary + lineEnd);
                outputStream.writeBytes("Content-Disposition: form-data; name=\"language\""+lineEnd);
                outputStream.writeBytes(lineEnd);
                outputStream.writeBytes("en"+lineEnd);
                */
                //PARAMETER2
                outputStream.writeBytes(twoHyphens + boundary + lineEnd);
                outputStream.writeBytes("Content-Disposition: form-data; name=\"apikey\""+lineEnd);
                outputStream.writeBytes(lineEnd);
                outputStream.writeBytes(apiKey+lineEnd);

                //END PARAMETER
                outputStream.writeBytes(twoHyphens + boundary + lineEnd);

                // Responses from the server (code and message)
                Integer serverResponseCode = connection.getResponseCode();
                // Read the response
                InputStream is = connection.getInputStream();
                ByteArrayOutputStream baos = new ByteArrayOutputStream();
                byte[] bytes = new byte[2048];
                int bytesReadd;
                while((bytesReadd = is.read(bytes)) != -1) {
                    baos.write(bytes, 0, bytesReadd);
                }
                byte[] bytesReceived = baos.toByteArray();
                baos.close();

                is.close();
                String response = new String(bytesReceived);
                JSONObject jsonObj=new JSONObject(response);
                JSONArray jsnArr = jsonObj.getJSONArray("ParsedResults");
                JSONObject jsnfinal=jsnArr.getJSONObject(0);
                String finalresp=jsnfinal.getString("ParsedText");

                Log.d("message ","RESPONSE message"+finalresp);


                 filteredResponse=finalresp.replaceAll("[^a-zA-Z\\s]+|[^a-zA-Z\\s]+", "").toLowerCase();
               filteredResponse=filteredResponse.replaceAll("\r\n|\n"," ");
                //Log.d("REQUEST " ,connection.getRequestProperties().toString());
                Log.d("CODE ","RESPONSE CODE"+serverResponseCode);
                Log.d("message ","Filtered RESPONSE message"+filteredResponse);
                //filteredResponse="Dubai";
                fileInputStream.close();
                outputStream.flush();
                outputStream.close();
            }
            catch (Exception ex)
            {
                Log.e("Major exception","exection" + ex.toString());
                //Exception handling
            }

            Log.e("filter in back","filteredResponse" + filteredResponse);
            return filteredResponse;
        }

    }
}