import React from "react"
import Navbar from "./component/Navbar"
import Card from "./component/Card"
import Search from "./component/Search"
import axios from "axios";
import { useEffect, useState } from "react"
import "primereact/resources/themes/lara-light-indigo/theme.css";  //theme
import "primereact/resources/primereact.min.css";                  //core css
import "primeicons/primeicons.css";                                //icons

export default function App() {
    const [data,setData]= useState([])
    const [search, setSearch] = useState("")
    const [noOfFeeds, setNoOfFeeds] = useState(0);
    const [loading , setLoading]=useState(false);
    const [endOfList,setEndOfList] = useState(false);

    useEffect(() => {
       sendSearch(0)
      },[search])

    console.log(search)

    const sendSearch = async(number)=>{
       
        let searchApi = await axios.post('/Rss_Feed_route/',{search:search, count:number+10});
        console.log(searchApi.data.data);
        if(searchApi.data.data.length < 10  ){
            setEndOfList(true);  
            console.log("SendSearch  if Stat:  ",searchApi.data.data.length < 10)    
          }
        else if(searchApi.data.data.length === data.length && searchApi.data.data.length <=10 && search !== ""){
            setEndOfList(true);

        }
        else{
            setEndOfList(false);
        }
        
        setNoOfFeeds(number+10)
       setData(searchApi.data.data)
    }
   
    const seeMore =async ()=>{
        setLoading(true);
        setEndOfList(false)
        await sendSearch(noOfFeeds)
        setLoading(false);
    }
    
    const cards = data.map(item => {

        return (
            <Card
                key={item._id}
                {...item}
            />    
        )
      
    })

    window.localStorage.setItem("search","")

    return (
        <div>
            <Navbar /> 
            <Search 
                 setSearch={setSearch}
                 search = {search}
            />
            <section className="cards-list">
                {cards}
            </section>
            { endOfList? null:<button className="seeMore"
            onClick={()=> seeMore()}>{loading? "loading" :"See More"}</button>}
        </div>
    )
}