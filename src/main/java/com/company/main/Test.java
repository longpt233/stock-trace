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

        System.out.println("\n ------------------------------------\n| content / total (Block) = " + cnt + " / " + listTextBlock.size() + " |\n ------------------------------------");

    }

    public static void main(String[] args) throws IOException {
        Test.run("https://vnexpress.net/co-phieu-vingroup-do-thi-truong-4364875.html");
    }
}
