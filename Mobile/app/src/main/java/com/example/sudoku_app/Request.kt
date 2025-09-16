package com.example.sudoku_app

import com.google.gson.annotations.SerializedName

data class Request (
    @SerializedName("mode"   ) var mode   : Int?    = null,
    @SerializedName("values" ) var values : String? = null,
    @SerializedName("level"  ) var level  : Int?    = null
)