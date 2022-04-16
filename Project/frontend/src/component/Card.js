/* eslint-disable jsx-a11y/alt-text */

import React from "react"
//import data from "../data"
import img from '../image/default.jpg'
export default function Card(props) {


    var source = (props.Link).slice((props.Link).indexOf("://") + 3)
    //var image = "./src/image/d.png"
    var descrp = props.Description
    var d = (props.PubDate).slice(0, 16)
    var t = (props.PubDate).slice(16, 25)
    var image = props.Image
    const fallbackimg = (e)=>{
        e.target.src = img
    }
    //console.log(image)

    // if((props.Description).includes("<img") || (props.Description).includes("< img"))
    // {
    //     image = (props.Description).slice((props.Description).indexOf("\"") + 1, (props.Description).indexOf("\" />")) 
    //     descrp = (props.Description).slice((props.Description).indexOf("<br/>") + 6, (props.Description).indexOf("<a"))
    // }
    if(descrp.length >300)
        descrp = descrp.substr(0, 300) + "..."

        return (
            <div className="card ">

                <div className="card--img">
                    <img
                        className="card--img--style"
                        src={props.Image}
                        onError= {e => fallbackimg(e)}
                    />
                </div>

                <div className="card--data ">
                    <a className="card--title" href={props.Link} target="_blank" rel="noreferrer">{props.Title}</a>
                    <p className="card--description">{descrp}</p>

                    <div className="card--stats flex ">
                        <span className="card--source">Source: <a className="card--sourceLink" href={"https://" + source.slice(0, source.indexOf("/"))} target="_blank" rel="noreferrer" > {source.slice(0, source.indexOf("/"))} </a></span>
                        <span className="card--datetime text-right">{d} | {t} GMT</span>
                    </div>
                </div>
            </div>
        )
        
       
        
        
    
}