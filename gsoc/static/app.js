"use strict";

class Feed extends React.Component {
	constructor(props){
		super(props);
		this.state = {
			entries: []
		};
	}
	componentWillMount() {
		fetch(this.props.url).then(response => {
			response.text().then(text => {
				let p = new DOMParser();
				let rss = p.parseFromString(text, "text/xml");
				let entries = [].slice.call(rss.getElementsByTagName("entry"));
				this.setState({entries});

				//debug
				window.entries = this.state.entries;
			});
		});
	}
	render() {
		let entries = this.state.entries;
		entries = entries.filter(this.props.filter || (x => true));
		entries = entries.map((entry, id) => <Entry key={id} data={entry}/>);
		
		// Use class names matching the GitHub HTML
		return (
		<div className="news">
			<h1>Honeynet GSoC Activity Feed</h1>
			{entries}
		</div>
		);
	}
}

class Entry extends React.Component {
	render(){
		let content = this.props.data.getElementsByTagName("content")[0].textContent;
		let html = {__html: content};

		// Use class names matching the GitHub HTML
		return (
		<div className="alert">
			<div className="body" dangerouslySetInnerHTML={html}/>
		</div>
		);
	}
}

function authors(names){
	names = names.split(" ");
	return function(entry){
		let author = entry.querySelector("author name").textContent;
		return names.indexOf(author) > -1;
	}
}


//let filter = authors("Kriechi");
let filter = false;
React.render(
	<Feed url="/feed" filter={filter} />,
	document.getElementById("main")
);