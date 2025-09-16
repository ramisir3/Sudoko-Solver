package com.example.sudoku_app

import android.annotation.SuppressLint
import android.os.Bundle
import android.text.Editable
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.gridlayout.widget.GridLayout
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

import java.util.Timer
import kotlin.concurrent.schedule

class SolveMode : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_solve_mode)
        val editTextList = ArrayList<EditText>()
        val grid = findViewById<GridLayout>(R.id.sudoku)
        val confirm = findViewById<Button>(R.id.confirmBtn)
        val getGrid = findViewById<Button>(R.id.get_grid)

        getGrid.isClickable =false
        confirm.isClickable =false

        for (i in 0 until grid.childCount) {
            if (grid.getChildAt(i) is EditText) {
                editTextList.add(grid.getChildAt(i) as EditText)
            }
        }

        Timer("Setting Up", false).schedule(30000) {
            getGrid.isClickable =true
            confirm.isClickable =true
        }

        getGrid.setOnClickListener {
            API.getApi()?.getAllValues()?.enqueue(
                object : Callback<com.example.sudoku_app.Response> {
                    override fun onResponse(
                        call: Call<com.example.sudoku_app.Response>,
                        response: Response<com.example.sudoku_app.Response>
                    ) {
                        if (response.isSuccessful) {
                            println("received values")
                            val values:String = response.body()?.values.toString()

                            for(i in 0 until editTextList.size ){
                                editTextList[i].setText(values.substring(i,i+1))
                            }
                        }
                    }

                    override fun onFailure(call: Call<com.example.sudoku_app.Response>, t: Throwable) {
                        Toast.makeText(this@SolveMode,
                            "receive values Failed", Toast.LENGTH_SHORT).show()
                    }
                })
        }

        confirm.setOnClickListener {
            var output=""
            for(i in 0 until editTextList.size ){
                output += editTextList[i].text.toString()
            }

            val values=Request(1,output,0)
            API.getApi()?.sendAllValues(values)?.enqueue(object: Callback<Any> {

                override fun onResponse(call: Call<Any>, response: Response<Any>) {
                    if (response.isSuccessful) {
                        Toast.makeText(this@SolveMode,
                            "Confirmed", Toast.LENGTH_LONG).show()
                        this@SolveMode.finish()
                    }
                }

                override fun onFailure(call: Call<Any>, t: Throwable) {
                    Toast.makeText(this@SolveMode,
                        "Confirm Failed", Toast.LENGTH_SHORT).show()
                    println(t.message)
                }

            })
        }


    }
}