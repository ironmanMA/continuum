package com.continuum.utils;

import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import java.util.logging.StreamHandler;

/**
 * Created by vishnudutt on 06/02/16.
 */
public class TextHelper {

    public static LinkedList<String> Tokenizer(String garbage){

        garbage = garbage.replaceAll("[^a-zA-Z0-9\\s]+|[^a-zA-Z0-9\\s]+", "").toLowerCase();

        System.out.println(garbage);

        LinkedList tokens = new LinkedList<String>();



        tokens.addAll(Arrays.asList(garbage.split("\\s+")));
        System.out.println(tokens);

        String[] stopWords = {"a","able","about","across","after","all","almost","also","am","among","an","and","any","are","as","at","be","because","been","but","by","can","cannot","could","dear","did","do","does","either","else","ever","every","fr","from","get","got","had","has","have","he","her","hers","him","his","how","however","i","if","in","into","is","it","its","just","least","let","like","likely","may","me","might","most","must","my","neither","no","nor","not","of","off","often","on","only","or","other","our","own","rather","said","say","says","she","should","since","so","some","than","that","the","their","them","then","there","these","they","this","tis","to","too","twas","us","wants","was","we","were","what","when","where","which","while","who","whom","why","will","with","would","yet","you","your"};
        tokens.removeAll(Arrays.asList(stopWords));

        System.out.println(tokens);

        return  tokens;
    }


    public static LinkedList<String> getMovies(LinkedList<String> tokens){

        String[] movies = {"cindrella","revenant","joy","airlift"};
        LinkedList<String> intersection = new LinkedList<String>(Arrays.asList(movies));
        intersection.retainAll(tokens);
        return  intersection;
    }

    public static LinkedList<String> getPlaces(LinkedList<String> tokens){

        //String[] places = {"paris","bhutan","trolltunga","koramangala"};

        String[] places = {"Abilene"};
        LinkedList<String> intersection = new LinkedList<String>(Arrays.asList(places));
        intersection.retainAll(tokens);
        return  intersection;
    }

    public static LinkedList<String> getFood(LinkedList<String> tokens){

        String[] food = {"dinner","Chiantis","pizza","pasta"};
        LinkedList<String> intersection = new LinkedList<String>(Arrays.asList(food));
        intersection.retainAll(tokens);
        return  intersection;
    }
}
