import Navbar from "./Navbar"

function Layout({ children }) {
	return (
		<div>
			<Navbar />

			<div className="page-content">
				{children}
			</div>
		</div>
	)
}

export default Layout