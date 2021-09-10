package com.company.main;

import com.company.model.elements.TextBlock;
import com.company.model.elements.TextDocument;
import com.company.parse.ParseWebsite;
import org.jsoup.nodes.Element;

import java.io.IOException;
import java.util.List;

public class Test {

    public static void run(String url){

        ParseWebsite parse = new ParseWebsite(url);
        List<Element> listElement = parse.getListElements();
        TextDocument document = new TextDocument(listElement);
        List<TextBlock> listTextBlock = document.getListTextBlocks();

        int cnt = 0;
        for(TextBlock t : listTextBlock) {
            if(t.isContent()) {
                System.out.println(t.getText());
                cnt++;
            }
        }

        System.out.println("\n ------------------------------------\n| content / total (Block) = " + cnt + " / " + listTextBlock.size() + " |");

    }

    public static void main(String[] args) throws IOException {
        Test.run("https://batdongsan.com.vn/ban-can-ho-chung-cu-duong-dien-bien-phu-phuong-25-prj-khu-phuc-hop-152-dien-bien-phu/ban-152-nhan-nha-2021-thanh-toan-1-7-ty-nhan-nha-chiet-khau-8-5-0776254588-pr29535244");
    }
}
