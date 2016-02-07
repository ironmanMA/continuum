package com.continuum.base;

/**
 * Created by vishnudutt on 06/02/16.
 */
public class TermInput {

    private String userName;
    private String geoLocation;
    private String text;


    public TermInput() {
    }

    public TermInput(String userName, String geoLocation, String text) {
        this.userName = userName;
        this.geoLocation = geoLocation;
        this.text = text;
    }

    public String getUserName() {
        return userName;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }

    public String getGeoLocation() {
        return geoLocation;
    }

    public void setGeoLocation(String geoLocation) {
        this.geoLocation = geoLocation;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }
}
