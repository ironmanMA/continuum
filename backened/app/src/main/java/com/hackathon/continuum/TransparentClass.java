package com.hackathon.continuum;

import android.app.Activity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import com.hackathon.continuum.R;
import android.view.View;
import android.graphics.Bitmap;
import java.io.*;
import android.provider.MediaStore;
import android.os.Environment;
import android.graphics.Bitmap.CompressFormat;
public class TransparentClass extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_transparent);

    }

    public Bitmap takeScreenshot() {
        View rootView = findViewById(android.R.id.content).getRootView();
        rootView.setDrawingCacheEnabled(true);
        return rootView.getDrawingCache();
    }
    public void saveBitmap(Bitmap bitmap) {
        File imagePath = new File("/storage/sdcard0/hojaoimg1.png");
        FileOutputStream fos;
        try {
            fos = new FileOutputStream(imagePath);
            bitmap.compress(CompressFormat.JPEG, 100, fos);
            fos.flush();
            fos.close();
        } catch (FileNotFoundException e) {
            //Log.e("GREC", e.getMessage(), e);
        } catch (IOException e) {
            //Log.e("GREC", e.getMessage(), e);
        }
    }

}
