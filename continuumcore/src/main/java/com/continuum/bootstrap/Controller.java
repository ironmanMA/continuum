package com.continuum.bootstrap;

import com.continuum.base.TermInput;
import com.continuum.base.TermResponse;
import com.continuum.utils.TextHelper;
import com.google.gson.Gson;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import javax.ws.rs.Consumes;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import java.util.LinkedList;
import java.util.List;

/**
 * Created by vishnudutt on 06/02/16.
 */

public class Controller {

    @POST
    @Path("/status")
    @Produces({"application/xml","application/json"})
    @Consumes({"application/json"})

    public String test(){
        return "Vishnu Dutt";
    }

    @POST
    @Path("/highterms")
    @Produces({"application/xml","application/json"})
    @Consumes({"application/json"})
    public String highTerms(TermInput garbage){


        System.out.println(garbage);

        Gson gson = new Gson();
        LinkedList<String> movies = new LinkedList<String>();
        LinkedList<String> places = new LinkedList<String>();
        LinkedList<String> food = new LinkedList<String>();
        LinkedList<String> tokens = new LinkedList<String>();


        tokens = TextHelper.Tokenizer(garbage.getText());

        movies = TextHelper.getMovies(tokens);
        places = TextHelper.getPlaces(tokens);
        food = TextHelper.getFood(tokens);


        TermResponse tr = new TermResponse(garbage.getUserName(),garbage.getGeoLocation(),movies,places,food);

        String toReturn = gson.toJson(tr);
        return toReturn;
    }

}



