import React, { useContext, useEffect, useState} from 'react';
import { PageContext } from './App';
import ErImg from "./assets/error_image.jpg";

export default function SideView() {
    const {log, setLog, currentPage, setCurrentPage} = useContext(PageContext);
    const [isStreaming, setIsStreaming]=useState(false);
	const [feedbackText, setFeedbackText] = useState('');
	useEffect(() => {
		fetch('http://localhost:5000/start_feed')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'video feed started') {
                    setIsStreaming(true);
					console.log("on");
                }
            })
            .catch(error => console.log(error));
        return () => {
            // Stop video feed when component unmounts
            fetch('http://localhost:5000/stop_feed')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'video feed stopped') {
                        setIsStreaming(false);
						console.log("off")
                    }
                })
                .catch(error => console.log("error"));
        };
        setCurrentPage('SideView');        
    }, [currentPage]);
	
	useEffect(()=>{
		const interval = setInterval(() => {
            fetch('http://localhost:5000/feedback')
				.then(response=>response.json())
				.then(data=>{
					setFeedbackText(data.status);
				})
				.catch(error =>console.log("error"));
        }, 500);
		return () => clearInterval(interval);
	},[]);
	
    return (
        <div className="lg:px-20 px-8 md:text-base text-xs lg:text-base">
            <h1 className="text-[rgb(212,195,87)] mt-4 mb-2 text-lgm lg:text-xl font-bold"
			style={{ fontFamily: 'Trebuchet MS, Sans-serif' }}>Side View</h1>
			<div className="video-container border-4 border-gray-400 rounded-md p-2">
                {isStreaming ? (
					<>
                    <img src={`http://localhost:5000/get_feed?${Date.now()}`} alt="Feed From Py Back End" className="mx-auto" />
					<p  className="mt-4 text-lg text-[rgb(255,255,255)] font-semibold">{feedbackText}</p>
					</>
                ) : (
					<>
                    <img src={ErImg} alt="Error Image" className="mx-auto w-80 h-60"/>
					<p  className="mt-4 text-lg text-[rgb(255,255,255)] font-semibold">Opening Webcam</p>
					</>
                )}
            </div>
        </div>
    );
}