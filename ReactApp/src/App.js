import { cards } from './CardCatalogue';
import data from "./recs/recommendations_Graham.json";
import './App.css';
import { useState } from 'react';


function App() {
  const cardId = data.recommendations.map(r => r.card_id);
  const headerText = ['Top Recommendation', 'Great Alternative', 'Final Top Choice'];
  const [index, setIndex] = useState(0);
  const item = data.recommendations.find(r => r.card_id === cardId[index]);
  const selectedCard = cards.find(card => card.id === cardId[index]);
  

  const handleNext = () => {
    setIndex((prevIndex) => (prevIndex + 1) % cardId.length);
  }

  const handlePrev = () => {
    if(index == 0){
      setIndex(2);
    }else{
      setIndex((prevIndex) => (prevIndex - 1));
    }
  }

  return( 
    <div>
      <header className="App-header">
        <div className="Button-left">
          <button onClick={handlePrev}
            style={{
              display: 'flex',
              justifyContent: 'flex-end',
              alignItems: 'center',
              paddingRight: '20px'
            }}
          >  
           <div class="button-box">
    <span class="button-elem">
      <svg viewBox="0 0 46 40" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M46 20.038c0-.7-.3-1.5-.8-2.1l-16-17c-1.1-1-3.2-1.4-4.4-.3-1.2 1.1-1.2 3.3 0 4.4l11.3 11.9H3c-1.7 0-3 1.3-3 3s1.3 3 3 3h33.1l-11.3 11.9c-1 1-1.2 3.3 0 4.4 1.2 1.1 3.3.8 4.4-.3l16-17c.5-.5.8-1.1.8-1.9z"
        ></path>
      </svg>
    </span>
    <span class="button-elem">
      <svg viewBox="0 0 46 40">
        <path
          d="M46 20.038c0-.7-.3-1.5-.8-2.1l-16-17c-1.1-1-3.2-1.4-4.4-.3-1.2 1.1-1.2 3.3 0 4.4l11.3 11.9H3c-1.7 0-3 1.3-3 3s1.3 3 3 3h33.1l-11.3 11.9c-1 1-1.2 3.3 0 4.4 1.2 1.1 3.3.8 4.4-.3l16-17c.5-.5.8-1.1.8-1.9z"
        ></path>
      </svg>
    </span>
  </div>
          </button>
        </div>

        <div className="text">
          <h1>
            {headerText[index]}
          </h1>
          <div class="glow-container">
            <div class="glow"></div>
            <img src={selectedCard.image} className="main-image" alt="logo" />
          </div>
          <h2>
            {selectedCard.name} 
          </h2>

          <p>
            <ul>{item.reason[0]}</ul>
            <ul>{item.reason[1]}</ul>
            <ul>{item.reason[2]}</ul>
          </p>
        </div>

        <div className="Button-right">
          <button onClick={handleNext}
            style={{
              display: 'flex',
              justifyContent: 'flex-end',
              alignItems: 'center',
              paddingRight: '20px'
            }}
          >  
            <div class="button-box">
    <span class="button-elem-right">
      <svg viewBox="0 0 46 40" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M46 20.038c0-.7-.3-1.5-.8-2.1l-16-17c-1.1-1-3.2-1.4-4.4-.3-1.2 1.1-1.2 3.3 0 4.4l11.3 11.9H3c-1.7 0-3 1.3-3 3s1.3 3 3 3h33.1l-11.3 11.9c-1 1-1.2 3.3 0 4.4 1.2 1.1 3.3.8 4.4-.3l16-17c.5-.5.8-1.1.8-1.9z"
        ></path>
      </svg>
    </span>
    <span class="button-elem">
      <svg viewBox="0 0 46 40">
        <path
          d="M46 20.038c0-.7-.3-1.5-.8-2.1l-16-17c-1.1-1-3.2-1.4-4.4-.3-1.2 1.1-1.2 3.3 0 4.4l11.3 11.9H3c-1.7 0-3 1.3-3 3s1.3 3 3 3h33.1l-11.3 11.9c-1 1-1.2 3.3 0 4.4 1.2 1.1 3.3.8 4.4-.3l16-17c.5-.5.8-1.1.8-1.9z"
        ></path>
      </svg>
    </span>
  </div>
          </button>
        </div>

      </header>
    </div>
  );
}

export default App;
