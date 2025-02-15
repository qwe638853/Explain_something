import { ethers } from  "ethers";
import { WebSocketServer } from "ws";
import express  from "express";

const app = express();
const PORT = 4000;



const Infura_API = "a30ec425abb446028c17190b513c001f";
const Etherscan_API = "RKFRN7F2EGCMFWPMVTX5RE4ZIQ7E1RHJXI";
const wsProvider = new ethers.WebSocketProvider(`wss://mainnet.infura.io/ws/v3/${Infura_API}`);
const esProvider = new ethers.EtherscanProvider("homestead",Etherscan_API);
const userAddress = "0x55b7441C7F9c14343d888179C69E7c233595aFE6"
//const wss = new WebSocketServer({port:4001});



const now = Math.floor(Date.now());
//time_size
const DAY_TIME = 24 * 60 * 60;
const WEEK_TIME = 7 * DAY_TIME;
const MONTH_TIME = 31 * WEEK_TIME;



async function transactoinFilter(timeSize){
    try{
        var transactionList = await esProvider.fetch('account',{
            action: "txlist",
            address: userAddress
        });

        const startTime = now - timeSize;

      

    }catch(err){
        console.error("Error fetching transactions:", err);
        return [];
    }
    
}


