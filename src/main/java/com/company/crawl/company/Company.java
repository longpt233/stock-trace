package com.company.crawl.company;

public class Company {

    private String id ;
    private String category;
    private double price;
    private String soNhanVien;

    public Company(String id, String category, double price, String soNhanVien) {
        this.id = id;
        this.category = category;
        this.price = price;
        this.soNhanVien = soNhanVien;
    }

    public double getPrice() {
        return price;
    }

    public void setPrice(int price) {
        this.price = price;
    }

    public String getSoNhanVien() {
        return soNhanVien;
    }

    public void setSoNhanVien(String soNhanVien) {
        this.soNhanVien = soNhanVien;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    @Override
    public String toString() {
        return id + ',' + category +','+ price+ ","+ soNhanVien;
    }


}
