import React, { useState } from "react"
import { InputText } from 'primereact/inputtext';
import axios from "axios";

// import { Dropdown } from 'primereact/dropdown';
// import { PrimeIcons } from 'primereact/api';
// import { RadioButton } from 'primereact/radiobutton';

export default function Search(props) {

    //const [value, setValue] = useState("")
   // console.log(value)
//     const sendSearch = async(e)=>{
//         const search = e;
//         setValue(search);
// //router.post('/Rss_Feed_route', fetch_rss_feed);
//         const searchApi = await axios.post('/Rss_Feed_route/',{search:search});
//         console.log(searchApi.data.data);
//     }
    return (
        <div className="search p-3 justify-content-between flex align-items-center">
            <InputText 
                className="border-300 border-round w-12"
                value={props.search}
               //onChange={(e) => { setValue(e.target.value); props.enter(value)}}
                onChange={(e) => {props.setSearch(e.target.value)}}

                // onKeyDown={(e) => {
                //     if (e.key === 'Enter') {
                //         window.localStorage.setItem("search", e.target.value);
                //        // props.enter()
                //         //window.location.reload()
                //     }
              // }}
                placeholder="Search"
            />
            {/* <button className="searchBtton" 
                            onClick={(e) => { props.sendSearch()}}

            > search </button> */}
            {/* <div className="divider"></div>

            <label 
                className="text-xl "
            >
                Sort By: 
            </label>

            <Dropdown 
                className="search--dropdown w-2"
                value={sortBy} 
                options={sort} 
                onChange={(e) => setSort(e.value)} 
                optionLabel="name" 
            /> */}
        </div>
    )
}