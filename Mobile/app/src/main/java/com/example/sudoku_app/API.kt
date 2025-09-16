package com.example.sudoku_app

import com.google.gson.Gson
import com.google.gson.GsonBuilder
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object API {
    private const val BASE_URL ="http://192.168.238.112"
    private var gson: Gson = GsonBuilder()
        .setLenient()
        .create()

    private val api = Retrofit.Builder()
        .addConverterFactory(GsonConverterFactory.create(gson))
        .baseUrl(BASE_URL)
        .build()
        .create(Requests::class.java)

    fun getApi(): Requests? {
        return api
    }
}
