package com.company.crawl.category;

public class Category {

    private String category;
    private String categoryEng;
    private String vonHoaThiTruong;
    private String tiSuatCoTuc;
    private String rateChange;
    private String volume;
    private int congNghiep;
    private int coPhieu;

    public Category(){

    }

    public Category(String category,String categoryEng, String vonHoaThiTruong, String tiSuatCoTuc, String rateChange, String volume, int congNghiep, int coPhieu) {
        this.category = category;
        this.vonHoaThiTruong = vonHoaThiTruong;
        this.tiSuatCoTuc = tiSuatCoTuc;
        this.rateChange = rateChange;
        this.volume = volume;
        this.congNghiep = congNghiep;
        this.coPhieu = coPhieu;
        this.categoryEng = categoryEng;
    }

    public String getCategoryEng() {
        return categoryEng;
    }

    public void setCategoryEng(String categoryEng) {
        this.categoryEng = categoryEng;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getVonHoaThiTruong() {
        return vonHoaThiTruong;
    }

    public void setVonHoaThiTruong(String vonHoaThiTruong) {
        this.vonHoaThiTruong = vonHoaThiTruong;
    }

    public String getTiSuatCoTuc() {
        return tiSuatCoTuc;
    }

    public void setTiSuatCoTuc(String tiSuatCoTuc) {
        this.tiSuatCoTuc = tiSuatCoTuc;
    }

    public String getRateChange() {
        return rateChange;
    }

    public void setRateChange(String rateChange) {
        this.rateChange = rateChange;
    }

    public String getVolume() {
        return volume;
    }

    public void setVolume(String volume) {
        this.volume = volume;
    }

    public int getCongNghiep() {
        return congNghiep;
    }

    public void setCongNghiep(int congNghiep) {
        this.congNghiep = congNghiep;
    }

    public int getCoPhieu() {
        return coPhieu;
    }

    public void setCoPhieu(int coPhieu) {
        this.coPhieu = coPhieu;
    }

    @Override
    public String toString() {
        return  category + ','  +
                categoryEng + ','+
                vonHoaThiTruong + ',' +
                tiSuatCoTuc + ',' +
                rateChange + ',' +
                volume + ',' +
                congNghiep + ',' +
                coPhieu;
    }
}
