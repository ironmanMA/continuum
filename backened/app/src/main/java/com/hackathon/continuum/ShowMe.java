package com.hackathon.continuum;

import android.app.ActionBar;
import android.app.Activity;
import android.widget.PopupWindow;
import android.os.Bundle;
import android.view.Gravity;
import android.webkit.WebViewClient;
import android.webkit.WebView;
import android.view.View;
import android.net.http.SslError;
import android.webkit.SslErrorHandler;
import android.webkit.WebSettings;
import android.webkit.WebChromeClient;
import android.view.WindowManager;
import android.util.Log;
import android.graphics.Point;
import android.view.Display;
import android.net.Uri;
import android.content.Intent;
import android.accounts.Account;
import android.accounts.AccountManager;
import android.widget.Toast;
import android.app.Dialog;
import java.util.List;
import java.util.LinkedList;
/**
 * Created by gaurav on 2/7/16.
 */
public class ShowMe extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        String response;
        Bundle extras = getIntent().getExtras();

        if(extras == null) {
            response= null;
        } else {
            response= extras.getString("RESPONSE");
        }
        Log.d("RESPONSE IN INTENT","MY RESPONSE"+response);
        //getActionBar().hide();
        String userName=getUsername();
        //Toast.makeText(getApplicationContext(),"User "+userName,Toast.LENGTH_LONG).show();
        Display display = getWindowManager().getDefaultDisplay();
        Point size = new Point();
        display.getSize(size);
        WindowManager.LayoutParams params = new WindowManager.LayoutParams();
        params.x = -100;
        params.height = size.y/2;
        params.width = size.x;
        params.gravity= Gravity.BOTTOM;

        Dialog dialog = new Dialog(this);
        dialog.setContentView(R.layout.showme_layout);
        dialog.setCancelable(true);
        dialog.setTitle("Continuum");

        dialog.getWindow().setAttributes(params);


        //this.getWindow().setAttributes(params);
        //setContentView(R.layout.showme_layout);
        WebView webview = (WebView) dialog.findViewById(R.id.allresultswebview);
        webview.setVisibility(View.VISIBLE);
        WebSettings webSettings = webview.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);
        webview.setWebChromeClient(new WebChromeClient());
        webview.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                if(url.contains("continuum.rboomerang.com")) {
                    view.loadUrl(url);
                } else {
                    Intent i = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                    startActivity(i);
                }
                return true;
            }
            public void onReceivedSslError (WebView view, SslErrorHandler handler, SslError error) {
                handler.proceed() ;
            }
        });
        webview.loadUrl("http://continuum.rboomerang.com:8080/continuum?_user_="+userName+"&_geoLat_=12.9&_geoLon_=77.6&_text_="+response);


        dialog.show();
    }

    public String getUsername() {
        AccountManager manager = AccountManager.get(this);
        Account[] accounts = manager.getAccountsByType("com.google");
        List<String> possibleEmails = new LinkedList<String>();

        for (Account account : accounts) {
            possibleEmails.add(account.name);
        }

        if (!possibleEmails.isEmpty() && possibleEmails.get(0) != null) {
            String email = possibleEmails.get(0);
            String[] parts = email.split("@");
            if (parts.length > 0 && parts[0] != null)
                return parts[0];
            else
                return null;
        } else
            return null;
    }



}
