import React, { useContext, useEffect } from 'react';
import { PageContext } from './App';
import AboutImg from './assets/AboutImg.svg';
import './App.css';

export default function About() {
    const {log, setLog, currentPage, setCurrentPage} = useContext(PageContext);
    useEffect(() => {
        setCurrentPage('About');
    }, [currentPage]);
    return (
        <div className="lg:px-20 px-8 md:text-base text-xs lg:text-base">
            <h1 className="text-[rgb(212,195,87)] mt-4 mb-2 text-sm lg:text-lg font-bold">ABOUT</h1>
				<div className={`aboutp ${"rounded-lg flex justify-center items-center"}`}>
					<img className={`profimg ${"rounded-lg flex justify-center items-center"}`} src={AboutImg} style={{width:`18em`,height:`auto`,}}/>
					<div className={`abtxt ${"rounded-lg flex-col flex justify-center items-center"}`}>
						<p className="pb-3" style={{ fontWeight: 'bold', fontSize: '1.5em' }}>Rakshit Girish :&nbsp;</p>
						<p style={{fontSize: '1em' }}>About Rakshit Girish</p>
					</div>
				</div>
				<div className={`aboutp ${"rounded-lg flex justify-center items-center"}`}>
					<div className={`abtxt ${"rounded-lg flex-col flex justify-center items-center"}`}>
						<p className="pb-3" style={{ fontWeight: 'bold', fontSize: '1.5em' }}>Pushkar Urs :&nbsp;</p>
						<p style={{fontSize: '1em' }}>About Pushkar Urs</p>
					</div>
					<img className={`profimg ${"rounded-lg flex justify-center items-center"}`} src={AboutImg} style={{width:`18em`,height:`auto`,}}/>
				</div>
				<div className={`aboutp ${"rounded-lg flex justify-center items-center"}`}>
					<img className={`profimg ${"rounded-lg flex justify-center items-center"}`} src={AboutImg} style={{width:`18em`,height:`auto`,}}/>
					<div className={`abtxt ${"rounded-lg flex-col flex justify-center items-center"}`}>
						<p className="pb-3" style={{ fontWeight: 'bold', fontSize: '1.5em' }}>Rohit Rao :&nbsp;</p>
						<p style={{fontSize: '1em' }}>About Rohit Rao</p>
					</div>
				</div>
        </div>
    );
}
