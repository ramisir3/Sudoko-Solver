package com.example.sudoku_app

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Handler
import android.widget.Button
import android.widget.Toast
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response


class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val solve = findViewById<Button>(R.id.solveBtn)
        val generate = findViewById<Button>(R.id.puzzleBtn)
        solve.setOnClickListener {
            val intent = Intent(this@MainActivity, SolveMode::class.java)
            val values=Request(0,null,0)
            API.getApi()?.sendAllValues(values)?.enqueue(object: Callback<Any> {

                override fun onResponse(call: Call<Any>, response: Response<Any>) {
                    if (response.isSuccessful) {
                        Toast.makeText(this@MainActivity,
                            "Camera request accepted", Toast.LENGTH_LONG).show()
                        startActivity(intent)
                    }
                }

                override fun onFailure(call: Call<Any>, t: Throwable) {
                    Toast.makeText(this@MainActivity,
                        "Camera request Failed", Toast.LENGTH_SHORT).show()
                    println(t.message)
                    startActivity(intent)
                }

            })

        }

        generate.setOnClickListener{
            val intent = Intent(this@MainActivity, PuzzleMode::class.java)
            startActivity(intent)
        }

    }


}