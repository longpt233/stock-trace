package com.company.parse.support;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

public class SeleniumCrawler {

	WebDriver driver = null;

	public SeleniumCrawler() {
		String pathChromeDriver = null;
		String osname = System.getProperty("os.name").toLowerCase();

		if(osname.contains("linux")) {
			pathChromeDriver = "chromedriver/chromedriver_linux";
		} else {
			System.out.println("need driver for special os");
		}

		System.setProperty("webdriver.chrome.driver", pathChromeDriver);

		ChromeOptions options = new ChromeOptions();
		options.addArguments("headless");
		options.addArguments("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36");


		try {
			driver = new ChromeDriver(options);
		} catch (Exception e) {
			e.printStackTrace();
			return;
		}
	}
	
	public String getHTMLSource(String url) {

		driver.get(url);
		String html = driver.getPageSource();
		return html;
	}

	public void quitDriver(){
		driver.close();
	}

}
