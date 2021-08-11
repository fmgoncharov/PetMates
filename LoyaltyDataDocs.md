Разработчик: Гончаров Фёдор

Руководитель: Зотов Николай

Данные по программе лояльности

Поле _AuthStatus_:
* **Обязательное**
* Тип данных: **текстовый**
* Значения:
    * **member** — если пользователь авторизован в программе лояльности
    * **not_member** — если пользователь не авторизован в программе лояльности
    * **none** — например, если покупка осуществляется по подарочной карте

Поле _Coins_:
* **Необязательное**
* Тип данных: **числовой**
* Значения:
    * **<количество начисляемых монет>** — если значение _auth_status_ равно **member** или **not_member**

Примеры №1-3:

**Никакой содержательной информации не посылается** - выводится картинка-заглушка _"Скачивайте приложение..."_

Вообще не написано про LoyaltyData:

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
</Order>
```

Про LoyaltyData не написано ничего содержательного:

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

В AuthStatus записано значение не _member_ и не _not_member_. Для определённости пишем _none_. В поле **Coins** можно как передавать монеты, так и не передавать - влиять на работу программы не будет.

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
	<LoyaltyData/ AuthStatus="none">
</Order>
```

Пример №4:

Покупатель был авторизован по программе лояльности и получит 314.15 монет

Выводится позитивная картинка _"Вам начислено +314.15 монет"_

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

Пример №5:

Покупатель не был авторизован по программе лояльности, но мог потенциально получить 314.15 монет

Выводится грустная картинка _"Вам могло быть начислено +314.15 монет..."_

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
