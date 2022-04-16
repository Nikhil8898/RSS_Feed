import React, { useState } from "react"
import { InputText } from 'primereact/inputtext';

export default function Navbar() {

    const[value,setValue] = useState("")
    console.log(value)

    return (
        <nav className="nav">
            <h3 className="nav--title"> Inter Project #1 </h3>
        </nav>
    )
}