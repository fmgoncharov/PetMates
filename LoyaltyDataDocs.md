Разработчик: Гончаров Фёдор
Руководитель: Зотов Николай

Данные по программе лояльности
Документация

Поле _AuthStatus_:
* **Обязательное**
* Тип данных: **текстовый**
* Значения:
    * **member** — если пользователь авторизован в программе лояльности
    * **not_member** — если пользователь не авторизован в программе лояльности
    * **none** — если покупка осуществляется по подарочной карте

Поле _Coins_:
* **Необязательное**
* Тип данных: **числовой**
* Значения:
    * **<количество начисляемых монет>** — если значение _auth_status_ равно **member** или **not_member**

Пример №1:
Никакой содержательной информации не посылается: либо вообще не написано про LoyaltyData, либо просто <LoyaltyData/>
```
<?xml version="1.0" encoding="UTF-8"?>
<Order ID="000008719" PosID="998" SubTotal="1283" Total="1283" Discount="0" Status="Closed" SbpQRData="" SpbQRData="" CommonTender="">
	<Tenders>
		<Tender Total="91" Change="0" Name="Наличные"/>
	</Tenders>
	<CustomerDisplay>
		<LastItem Name="Блин с двойной красной икрой" Quantity="1" Amount="644"/>
		<Items>
			<Item Name="Блин с двойной красной икрой" Quantity="1" Amount="644"/>
		</Items>
	</CustomerDisplay>
	<KitchenDisplay>
		<Items>
			<Item Name="Блин двойной с кр икрой" Category="Блины" Packaging="Out"/>
		</Items>
	</KitchenDisplay>
	<LoyaltyData/>
</Order>
```

Пример №2:
Покупатель был авторизован по программе лояльности и получит 314.15 монет
```
<?xml version="1.0" encoding="UTF-8"?>
<Order ID="000008719" PosID="998" SubTotal="1283" Total="1283" Discount="0" Status="Closed" SbpQRData="" SpbQRData="" CommonTender="">
	<Tenders>
		<Tender Total="91" Change="0" Name="Наличные"/>
	</Tenders>
	<CustomerDisplay>
		<LastItem Name="Блин с двойной красной икрой" Quantity="1" Amount="644"/>
		<Items>
			<Item Name="Блин с двойной красной икрой" Quantity="1" Amount="644"/>
		</Items>
	</CustomerDisplay>
	<KitchenDisplay>
		<Items>
			<Item Name="Блин двойной с кр икрой" Category="Блины" Packaging="Out"/>
		</Items>
	</KitchenDisplay>
	<LoyaltyData/ AuthStatus="member" Coins="314.15">
</Order>
```

Пример №3:
Покупатель не был авторизован по программе лояльности, но мог потенциально получить 314.15 монет
```
<?xml version="1.0" encoding="UTF-8"?>
<Order ID="000008719" PosID="998" SubTotal="1283" Total="1283" Discount="0" Status="Closed" SbpQRData="" SpbQRData="" CommonTender="">
	<Tenders>
		<Tender Total="91" Change="0" Name="Наличные"/>
	</Tenders>
	<CustomerDisplay>
		<LastItem Name="Блин с двойной красной икрой" Quantity="1" Amount="644"/>
		<Items>
			<Item Name="Блин с двойной красной икрой" Quantity="1" Amount="644"/>
		</Items>
	</CustomerDisplay>
	<KitchenDisplay>
		<Items>
			<Item Name="Блин двойной с кр икрой" Category="Блины" Packaging="Out"/>
		</Items>
	</KitchenDisplay>
	<LoyaltyData/ AuthStatus="not_member" Coins="314.15">
</Order>
```
