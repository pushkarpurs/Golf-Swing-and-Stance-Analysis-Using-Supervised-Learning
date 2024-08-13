import React, { useContext, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { PageContext } from './App';
export default function Home() {
    const {log, setLog, currentPage, setCurrentPage} = useContext(PageContext);
	//const [text, setText] = useState("Dynamic Text");
    useEffect(() => {
        setCurrentPage('Home');        
    }, [currentPage]);    
    return (
        <div className="lg:px-20 px-8 md:text-base text-xs lg:text-base">
            <h1 className="text-[rgb(212,195,87)] mt-4 mb-2 text-lgm lg:text-xl font-bold"
			style={{ fontFamily: 'Trebuchet MS, Sans-serif' }}>The Perfect Tool For Beginners</h1>
				<div className="bg-grey-400 p-4 pt-10 lg:prose-xl prose-p:text-grey-900 hover:prose-p:text-green-100 rounded flex justify-center items-center"
				style={{ fontFamily: 'Times New Roman, Serif' }}>
				
				<p className="text-lg pb-5 pt-3 lg:text-xl text-justify w-85 mx-auto">
				Golf is a sport with an incredibly high skill requirement. 
				It can be daunting for those who haven't played before, yet it 
				is also one of the most relaxing and enjoyable sports out there.
				If you're wondering how to get started, feeling intimidated by 
				experienced players at your local course, or having second thoughts
				about hitting the range while watching veterans effortlessly drive 
				the ball over a hundred yards, look no further. Our AI-powered golf 
				tutor is all you'll need to gain an edge over your rivals.
				Improve your handicap and become the king of your course with our tool.</p>
				
				</div>
				<div className="grid grid-cols-2 grid-rows-1 mt-8 mb-1 h-30">
					<div className="flex justify-center items-center h-20">
					<Link to="/side">
							<div className={`StkDisp hover:text-[rgb(255,100,100)] rounded-lg flex justify-center items-center w-64 h-12`}>
							<p>Side View</p></div>
					</Link>
					</div>
					<div className="flex justify-center items-center h-20">
					<Link to="/back">
							<div className={`StkDisp rounded-lg flex hover:text-[rgb(255,100,100)] justify-center items-center w-64 h-12`}>
							<p>Back View</p></div>
					</Link>
					</div>
				</div>
			<br />
        </div>
    );
}