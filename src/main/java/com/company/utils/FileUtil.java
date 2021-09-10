package com.company.utils;

import com.company.crawl.category.Category;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class FileUtil {

    public static List<Category> getListCategory(String path){
        List<Category> categories = new ArrayList<>();
        BufferedReader br = null;
        try {
            br = new BufferedReader(new FileReader(path));
            String line;
            while ((line = br.readLine()) != null) {
                String[] col = line.split(",");
                Category category = new Category(col[0],col[1], col[2], col[3] ,col[4],col[5], Integer.parseInt(col[6]), Integer.parseInt(col[7])  );
                categories.add(category);
            }

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (br != null) {
                    br.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return categories;
    }
}
