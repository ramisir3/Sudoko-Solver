package com.example.sudoku_app

import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import javax.security.auth.callback.Callback

interface Requests {

    @GET("values")
    fun getAllValues(): Call<Response>

    @POST("post")
    fun sendAllValues(@Body info: Request):Call<Any>
}