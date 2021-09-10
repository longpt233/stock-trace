package com.company.parse.support;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class TextNormalize {
	private static final Pattern REMOVE_TAGS = Pattern.compile("<.+?>");
	
	/* Normalize strings, remove space, enter beginning and end of line
	 * */
	public String normalize(String text) {
		text = replaceTag(text);
		text = delSpaceAndNewLine(text);
		text = removeDuplicate(text);
		text = removeCdata(text);
		
		return text;
	}
	
	/* if new line or space duplicate, we only keep one
	 * */
	private String removeDuplicate(String text) {
		// remove space if duplicate
		while(text.contains("  ")) {
			text = text.replace("  ", " ");
		}
		
		// remove space after \n
		while(text.contains("\n ")) {
			text = text.replace("\n ", "\n");
		}
		
		// remove \n if duplicate
		while(text.contains("\n\n")) {
			text = text.replace("\n\n", "\n");
		}
		
		return text;
	}
	
	/* remove cdata in html source
	 * */
	public String removeCdata(String text) {
		int start = 0;
		
		while(true) {
			start = text.indexOf("<![");
			int last = text.indexOf("]]>");
			
			if(start == -1) break;
			
			String sub = text.substring(start, last+3);
			text = text.replace(sub, "");
		}
		
		return text;
	}
	
	/* remove html tag in text
	 * */
	private String replaceTag(String text) {
		
		Matcher matcher= REMOVE_TAGS.matcher(text);
		return matcher.replaceAll("");
	}
	
	/* Delete space and new line beginning or end text
	 * */
	private String delSpaceAndNewLine(String text) {
		int lens = text.length();
		
		int start = 0;
		for(int i=0; i<lens; i++) { // find start
			if(text.charAt(i) != ' ' && text.charAt(i) != '\n') {
				start = i;
				break;
			}
		}
		
		int last = lens - 1;
		for(int i=lens-1; i>=0; i--) { // fine end
			if(text.charAt(i) != ' ' && text.charAt(i) != '\n') {
				last = i;
				break;
			}
		}
		
		String newText = text.substring(start, last+1);
		
		return newText;
	}
}
