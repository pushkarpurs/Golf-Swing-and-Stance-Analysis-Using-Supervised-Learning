import { Link, Routes, Route } from 'react-router-dom';
import { createContext, useState } from 'react';
import './App.css';
import Home from './Home';
import SideView from './SideView';
import BackView from './BackView';
import About from './About';
import Facebook from "./assets/Facebook.svg";
import AboutImg from "./assets/About.svg";
import InstaImg from "./assets/Instagram.svg";
import LinImg from "./assets/Linkedin.svg";
import TwitImg from "./assets/X.svg";
const PageContext = createContext();

function App() {
	const [log, setLog] = useState('HomePage');
	const [currentPage, setCurrentPage] = useState('Home');
	return (
		<PageContext.Provider value={{log, setLog, currentPage, setCurrentPage}}>
			<div className='min-h-screen flex flex-col justify-center'>
				<header className={`Head${'sticky top-0 w-full flex flex-col justify-center bg-[#000000]'}`}>
					<Link to="/">
						<h1 className='pt-5 text-[rgb(77,212,106)] text-s lg:text-3xl text-center font-bold'
						style={{ fontFamily: 'Courier New, monospace' }}>Golf Tutor</h1>
					</Link>
					<nav className='flex flex-wrap flex-shrink-10 items-center justify-between md:justify-start lg:justify-start my-4 mx-4 lg:p-4 p-0'>
						<Link className={currentPage == 'Home' ? 'sm:text-xs lg:text-lg text-[rgb(0,0,0)] hover:text-[rgb(255,255,255)]' : 'sm:text-xs lg:text-lg'} to="/">
							<div className='lg:px-6 px-2 bg-[rgb(220,220,220)] border-4 border-solid border-[rgb(100,100,100)]  hover:bg-[rgb(0,0,0)] rounded-xl'>HOME</div>
						</Link>
					</nav>
					<hr className='w-full'/>
				</header>
				<main className='flex-grow'>
					<Routes>
						<Route path="/" element={<Home />} />
						<Route path="/side" element={<SideView />} />
						<Route path="/back" element={<BackView />} />
						<Route path="/about" element={<About />} />
					</Routes>
				</main>
				<div className='bg-black mb-0 w-full mt-4'>
					<hr />
					<footer className='flex'>
						<div className={`foot-stuff`}>
							<Link className={`link ${'sm:text-xs lg:text-lg ml-8 mr-8 mb-8'}`} to="/about"><img className={`aboutimg`} src={AboutImg} alt="about" /></Link>
							{/* <div className='ml-auto flex flex-row justify-end'> */}
								{/* <a className={`imgs ${'sm:text-xs lg:text-lg ml-8 mr-8 mb-8'}`} target = "_blank" href="https://www.facebook.com/"><img className={`fbimg`} src={Facebook} alt="Facebook" /></a> */}
								<a className={`imgs ${'sm:text-xs lg:text-lg ml-8 mr-8 mb-8'}`} target = "_blank" href="https://www.instagram.com/"><img className={`igimg`} src={InstaImg} alt="Instagram" /></a>
								<a className={`imgs ${'sm:text-xs lg:text-lg ml-8 mr-8 mb-8'}`} target = "_blank" href="https://in.linkedin.com/"><img className={`inimg`} src={LinImg} alt="Linkedin" /></a>
								<a className={`imgs ${'sm:text-xs lg:text-lg ml-8 mr-8 mb-8'}`} target = "_blank" href="https://twitter.com/"><img className={`ximg`} src={TwitImg} alt="Twitter" /></a>
							{/* </div> */}
						</div>
					</footer>
				</div>
			</div>
		</PageContext.Provider>
	);
}

export { PageContext };
export default App;