package com.company.crawl.company;

import com.company.crawl.category.Category;
import com.company.utils.FileUtil;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class CrawlCompany {

    private List<Company> companies;

    public CrawlCompany(){
        companies = new ArrayList<>();
    }

    public void writeOut(String path) {
        BufferedWriter bw = null;
        try {
            bw = new BufferedWriter(new FileWriter(path));
            bw.flush();
            System.out.println("cate size = " + companies.size());
            for (Company it : companies) {
                bw.write(it + "\n");
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        } finally {
            try {
                if (bw != null) {
                    bw.close();
                }
            } catch (Exception ex1) {
                ex1.printStackTrace();
            }
        }

    }

    public void crawl(String category){

        String url = "https://vn.tradingview.com/markets/stocks-vietnam/sectorandindustry-sector/";
        try {
            Document doc = Jsoup.connect(url+category)
                    .userAgent("Mozilla/5.0")
                    .timeout(60 * 1000)
                    .get();
            Elements data = doc.select("#js-screener-container > div.tv-screener__content-pane > table > tbody > tr");

            for (Element it : data) {
                String id = it.select("td:nth-child(1)").text().split(" ")[1];
                String price = it.select("td:nth-child(2)").text();
                String soNhanVien = it.select("td:nth-child(10)").text();
                Company company = new Company(id, category,Double.parseDouble(price), soNhanVien);
                companies.add(company);
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    public static void main(String[] args) {
        CrawlCompany crawlCompany = new CrawlCompany();

        List<Category> categories = FileUtil.getListCategory("data/company/category.csv");
        for (Category i : categories){
            crawlCompany.crawl(i.getCategoryEng());
        }
        crawlCompany.writeOut("data/company/company-list.csv");
    }




}
