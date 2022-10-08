import './App.css';

import { useState} from 'react';
import { indexerClient, myAlgoConnect } from "./utils/constants";
import { microAlgosToString } from './utils/conversions';
import Cover from "./Cover";
import { addSecretAction, dislikeSecretAction, getSecretsAction, likeSecretAction, optIn } from './utils/marketplace';



function App() {

  const [address, setAddress] = useState(null);
  const [text, setText] = useState("");
  const [balance, setBalance] = useState(0);
  const [secrets, setSecrets] = useState([]);



  const fetchBalance = async (accountAddress) => {
    indexerClient.lookupAccountByID(accountAddress).do()
      .then(response => {
        const _balance = response.account.amount;
        setBalance(_balance);
      })
      .catch(error => {
        console.log(error);
      });
  };

  const connectWallet = async () => {
    myAlgoConnect.connect()
      .then(accounts => {
        const _account = accounts[0];
        setAddress(_account.address);
        fetchBalance(_account.address);
        if (_account.address) getSecrets(_account.address);
      }).catch(error => {
        console.log('Could not connect to MyAlgo wallet');
        console.error(error);
      })
  };

  const getSecrets = async (_address) => {
    try {
      alert("fetching animals")
      const secrets = await getSecretsAction();
      setSecrets(secrets);
    } catch (error) {
      alert(error)
      console.log(error);
    } finally {
      alert("fetched")
    }

  };

  const like = async (secret) => {
    await optIn(address, secret.appId)
    likeSecretAction(address, secret)
      .then(() => {
        getSecrets(address);
        fetchBalance(address);
      })
      .catch(error => {
        console.log(error)
        alert(error)
      })
  }

  const dislike = async (secret) => {
    dislikeSecretAction(address, secret)
      .then(() => {
        getSecrets(address);
        fetchBalance(address);
      })
      .catch(error => {
        console.log(error)
        alert(error)
      })
  }

  const submitForm = async (e) => {
    e.preventDefault();
    console.log(text);
    if (!text) return;
    try {
      await addSecretAction(address,{ secretText: text })
      getSecrets();
    } catch (error) {
      console.log(error);
    }
  }


  return (
    <>
      {address ? <div>
        {/* ======= Header ======= */}
        <header id="header" className="fixed-top d-flex align-items-center">
          <div className="container d-flex justify-content-between">
            <div className="logo">
              <h1><a href="/">Secrets</a></h1>
              {/* Uncomment below if you prefer to use an image logo */}
              {/* <a href="index.html"><img src="assets/img/logo.png" alt="" class="img-fluid"></a>*/}
            </div>
            <nav id="navbar" className="navbar">
              <ul>
                <li><a className="nav-link scrollto active" href="#hero">Home</a></li>
                <li><a className="nav-link scrollto" href="#contact">Balance: {microAlgosToString(balance)} NEAR</a></li>
              </ul>
              <i className="bi bi-list mobile-nav-toggle" />
            </nav>{/* .navbar */}
          </div>
        </header>{/* End Header */}
        {/* ======= Hero Section ======= */}
        <section id="hero" className="d-flex flex-column justify-content-center align-items-center">
          <div className="container text-center text-md-left" data-aos="fade-up">
            <h1>Welcome to Secrets</h1>
            <h2>Tell your story and earn from it</h2>
            <a href="#contact " className="btn-get-started scrollto">Get Started</a>
          </div>
        </section>{/* End Hero */}
        <main id="main">
          {/* ======= Steps Section ======= */}
          <section id="steps" className="steps section-bg">
            <div className="container">
              <div className="row no-gutters">
                {secrets.map(secret => <div className="col-lg-4 col-md-6 content-item" data-aos="fade-in" key={secret.appId}>
                  <span>{secret.secret}</span>
                  <p>{secret.appId}</p>
                  <br />
                  <div className='d-flex justify-content-between'>
                    <div>
                      <i onClick={() => like(secret)} class="bi bi-hand-thumbs-up"></i>{secret.likes}
                    </div>
                    <div><i onClick={() => dislike(secret)} class="bi bi-hand-thumbs-down"></i>{secret.dislikes}</div>

                  </div>


                </div>)}
              </div>
            </div>
          </section>{/* End Steps Section */}

          {/* ======= Contact Section ======= */}
          <section id="contact" className="contact">
            <div className="container">
              <div className="section-title" data-aos="fade-up">
                <h2>Add Your Secret </h2>
                <p>Add your secret to the pool</p>
              </div>
              <div className="row mt-5 justify-content-center" data-aos="fade-up">
                <div className="col-lg-10">
                  <form onSubmit={submitForm} role="form" className="php-email-form">
                    <div className="form-group mt-3">
                      <textarea className="form-control" onChange={(e) => setText(e.target.value)} name="message" rows={5} placeholder="Secrets..." required defaultValue={""} />
                    </div>
                    <div className="text-center"><button type="submit">Start Here</button></div>
                  </form>
                </div>
              </div>
            </div>
          </section>{/* End Contact Section */}
        </main>{/* End #main */}
      </div> :
        <Cover name={"Tell Your Secrets"} connect={connectWallet} />
      }
    </>
  );

}

export default App;
