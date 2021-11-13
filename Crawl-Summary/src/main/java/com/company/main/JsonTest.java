package com.company.main;


import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class JsonTest {

    public static void main(String[] args) {


        JSONParser parser = new JSONParser();

        try {
            Object obj = parser.parse(new FileReader("src/main/java/com/company/main/data.json"));

            JSONObject jsonObject =  (JSONObject) obj;

            System.out.println(jsonObject);

            Object name = jsonObject.get("name");
            System.out.println(name);

            JSONArray arr = (JSONArray) parser.parse(name.toString());


            System.out.println(arr.get(0));
            JSONObject userinfor =  (JSONObject) parser.parse(arr.get(0).toString());

            System.out.println(userinfor.get("first_name").toString());

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }
    }
}
