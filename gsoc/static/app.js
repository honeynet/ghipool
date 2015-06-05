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
				var p = new DOMParser();
				var rss = p.parseFromString(text, "text/xml");
				var entries = [].slice.call(rss.getElementsByTagName("entry"));
				this.setState({entries});

				//debug
				window.entries = this.state.entries;
			});
		});
	}
	render() {
		var entries = this.state.entries;
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
		var content = this.props.data.getElementsByTagName("content")[0].textContent;
		var html = {__html: content};

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
		var author = entry.querySelector("author name").textContent;
		return names.indexOf(author) > -1;
	}
}


//let filter = authors("Kriechi");
var filter = false;
React.render(
	<Feed url="/feed" filter={filter} />,
	document.getElementById("main")
);