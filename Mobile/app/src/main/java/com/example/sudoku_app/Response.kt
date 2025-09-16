package com.example.sudoku_app

import com.google.gson.annotations.SerializedName

data class Response (
    @SerializedName("values") var values : String? = null
    )