const { search } = require('../app');
var rssFeedModel= require('../model/Rss_feed_model');
module.exports={


    fetch_rss_feed: async function (req, res){

    let search = req.body.search?req.body.search:"blockchain"

    console.log(req.body.search)
    const count  = req.body.count
    //const score = {score: { $meta: "textScore"}}
    let qry = { $text: { $search: '"'+search+'"' } } ;

    console.log(search); 

     await rssFeedModel.aggregate( [
      { $match: qry },
      { $sort: { score: { $meta: "textScore" }} }
    ]).limit(count) 
      .then( item => res.json({data: item}) )
    .catch(error => console.log("Error", error))
      
    }
}