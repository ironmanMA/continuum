package com.continuum.base;

import java.util.LinkedList;
import java.util.List;

/**
 * Created by vishnudutt on 06/02/16.
 */
public class TermResponse {

    private String userName;
    private String geoLocation;
    private List<String> movies = new LinkedList<String>();
    private List<String> places = new LinkedList<String>();
    private List<String> food =  new LinkedList<String>();


    public TermResponse() {
    }

    public TermResponse(String userName, String geoLocation,  List<String> movies, List<String> places, List<String> food) {
        this.userName = userName;
        this.geoLocation = geoLocation;
        this.places = places;
        this.movies = movies;
        this.food = food;
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

    public List<String> getPlaces() {
        return places;
    }

    public void setPlaces(List<String> places) {
        this.places = places;
    }

    public List<String> getMovies() {
        return movies;
    }

    public void setMovies(List<String> movies) {
        this.movies = movies;
    }

    public List<String> getFood() {
        return food;
    }

    public void setFood(List<String> food) {
        this.food = food;
    }

    @Override
    public String toString() {
        return "TermResponse{" +
                "userName='" + userName + '\'' +
                ", geoLocation='" + geoLocation + '\'' +
                ", places=" + places +
                ", movies=" + movies +
                ", food=" + food +
                '}';
    }
}
