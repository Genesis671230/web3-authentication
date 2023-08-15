
const signInButton = document.getElementById("signInButton");

const verifyHashButton = document.getElementById("verifyHashButton");

window.ethereum.on('accountsChanged', function (accounts) {
  if (accounts.length > 0) {
      sessionStorage.setItem("walletAddress", accounts[0]);
  } else {
      sessionStorage.removeItem("walletAddress");
  }
})


const authButton = document.getElementById("authButton");


document.addEventListener("DOMContentLoaded", async function () {
  const signInButton = document.getElementById("signInButton");
  const verifyButton = document.getElementById("verifyButton");
  const nftsButton = document.getElementById("NftsButton");
  const challengeElement = document.getElementById("challenge");
  const nftsElement = document.getElementById("nfts");

  signInButton.addEventListener("click", async function () {
    try {
      const walletAddress = await getUserWalletAddress();
      if (!walletAddress) return;

      
      const response = await fetch("/generate_challenge/",{
        method:"POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ walletAddress: walletAddress}),
      });

      const challengeGen = await response.json()
      console.log(challengeGen,"this is challenge");
      const challenge = challengeGen.challenge;


      const challengeTxt = `Challenge: ${challenge}`;
      challengeElement.textContent = challengeTxt;
      sessionStorage.setItem("walletAddress", walletAddress);
      sessionStorage.setItem("challenge", challenge);
      
    } catch (error) {
      console.error(error);
    }
  });
  nftsButton.addEventListener("click", async function () {
    try {
      const access_token = sessionStorage.getItem("token");
     const res = await fetch("/nfts", {
        method: 'GET',
        headers: {
        'Authorization': `Token ${access_token}`
      }
    })
    const fetchedNfts = await res.json()
    
    fetchedNfts.map((data)=>{
      const card = document.createElement('div');

      card.classList.add('card'); 
      card.style.marginBottom = "2rem"
      card.style.display = "flex"
      card.style.flexDirection = "column"
      card.style.alignItems = "center"

      const name = document.createElement('h3');
      name.textContent = data.name;
      card.appendChild(name);
      
      const img = document.createElement('img');
      img.style.width = "10rem"
      img.style.height = "10rem"
      img.src = data.image_url;
      img.alt = data.name;
      card.appendChild(img);
      
      const description = document.createElement('p');
      description.textContent = data.description;
      card.appendChild(description);
    
      nftsElement.appendChild(card);
    })

    console.log(fetchedNfts)

    
  } catch (error) {
    console.error(error);
  }
});

  verifyButton.addEventListener("click", async function () {

    try {
      const walletAddress = sessionStorage.getItem("walletAddress");
      const challengeStr = sessionStorage.getItem("challenge");
      const challenge = `0x${challengeStr}`
      if (!walletAddress || !challenge) return;

      const accounts = await ethereum.request({ method: 'eth_accounts' });

      if (!accounts.length) {
          alert('No accounts found');
      } else {
          const walletAddress = accounts[0]; 
    
    const signature = await ethereum.request({
      method: 'personal_sign',
      params: [`challenge${challenge.toString()}`, walletAddress],
      });

      
      
      console.log(signature,challenge);
      const verificationResponse = await fetch("/verify_signature/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ walletAddress:walletAddress,signature:signature,hash:`challenge${challenge.toString()}` }),
      });
      
      
      if (verificationResponse.ok) {
        const tokenData = await verificationResponse.json();
        const token = tokenData.access_token;
        console.log("JWT Token:", token);
        sessionStorage.setItem("token", token);

        authButton.textContent = "Authenticated";
        authButton.classList.remove("bg-red-500");
        authButton.classList.add("bg-green-500");
        
      } else {
        console.error("Signature verification failed.");
      }
      
    }
    
          } catch (error) {
            console.error(error);
          }
        });
      });
      
      function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
          const cookies = document.cookie.split(";");
          for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
      }
    }
  }
  return cookieValue;
}

async function getUserWalletAddress() {
  try {
    if (window.ethereum) {
      await window.ethereum.enable();

      const accounts = await window.ethereum.request({
        method: "eth_requestAccounts",
      });
      return accounts[0];
    } else {
      console.error("Metamask not detected.");
      return null;
    }
  } catch (error) {
    console.error("Error getting wallet address:", error);
    return null;
  }
}

function generateUniqueHash(walletAddress) {
  const timestamp = new Date().getTime();
  const uniqueString = `${timestamp}-${walletAddress}`;

  const hashedString = hashFunction(uniqueString);

  return hashedString;
}

function hashFunction(input) {
  const hashed = CryptoJS.SHA256(input);
  return hashed.toString(CryptoJS.enc.Hex); 
}

async function signChallengeWithMetamask(challenge) {
  try {
    const walletAddress = await getUserWalletAddress();
    if (!walletAddress) return null;

    const message = `Challenge: ${challenge}`;
    const signature = verify(walletAddress, message);
    console.log(signature, "Signature");
    return signature;
  } catch (error) {
    console.error("Error signing challenge:", error);
    return null;
  }
}

const verify = (wallet, msg) => {
  const msgParams = JSON.stringify({
    domain: {
      chainId: 1,
      name: "Ether Mail",
      verifyingContract: "0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC",
      version: "1",
    },

    message: {
      contents: msg,

      from: {
        name: "Cow",
        wallets: [
          "0xCD2a3d9F938E13CD947Ec05AbC7FE734Df8DD826",
          "0xDeaDbeefdEAdbeefdEadbEEFdeadbeEFdEaDbeeF",
        ],
      },
      to: [
        {
          name: "Bob",
          wallets: [
            "0xbBbBBBBbbBBBbbbBbbBbbbbBBbBbbbbBbBbbBBbB",
            "0xB0BdaBea57B0BDABeA57b0bdABEA57b0BDabEa57",
            "0xB0B0b0b0b0b0B000000000000000000000000000",
          ],
        },
      ],
    },
    primaryType: "Mail",
    types: {
      EIP712Domain: [
        { name: "name", type: "string" },
        { name: "version", type: "string" },
        { name: "chainId", type: "uint256" },
        { name: "verifyingContract", type: "address" },
      ],
      Group: [
        { name: "name", type: "string" },
        { name: "members", type: "Person[]" },
      ],
      Mail: [
        { name: "from", type: "Person" },
        { name: "to", type: "Person[]" },
        { name: "contents", type: "string" },
      ],
      Person: [
        { name: "name", type: "string" },
        { name: "wallets", type: "address[]" },
      ],
    },
  });

  var params = [wallet, msgParams];
  var method = "eth_signTypedData_v4";

  web3.currentProvider.sendAsync(
    {
      method,
      params,
      from: wallet,
    },
    function (err, result) {
      if (err) return console.dir(err);
      if (result.error) {
        alert(result.error.message);
      }
      if (result.error) return console.error("ERROR", result);
      console.log("TYPED SIGNED:" + JSON.stringify(result.result));

      const recovered = sigUtil.recoverTypedSignature_v4({
        data: JSON.parse(msgParams),
        sig: result.result,
      });

      if (
        ethUtil.toChecksumAddress(recovered) ===
        ethUtil.toChecksumAddress(wallet)
      ) {
        alert("Successfully recovered signer as " + wallet);
      } else {
        alert(
          "Failed to verify signer when comparing " + result + " to " + wallet
        );
      }
    }
  );
};

function stringToHex(input) {
  let hex = "";
  for (let i = 0; i < input.length; i++) {
    hex += input.charCodeAt(i).toString(16);
  }
  return hex;
}
